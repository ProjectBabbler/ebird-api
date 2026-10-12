"""Various functions used in the API."""

import datetime as dt
import json
import threading
import time
from email.utils import parsedate_to_datetime
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ebird.api.requests import constants

# The maximum interval, in seconds, the rate limiter will slow down to
# after the eBird API responds with HTTP 429 Too Many Requests.
MAX_RATE_LIMIT_INTERVAL = 60.0


class RateLimitError(HTTPError):
    """Raised when the eBird API still responds with HTTP 429 Too Many
    Requests after all the retries have been used.

    It is a subclass of HTTPError so existing error handling still works.
    The retry_after attribute contains the number of seconds the API asked
    the caller to wait, or None if no Retry-After header was returned.

    """

    def __init__(self, exc, retry_after=None):
        super().__init__(exc.url, exc.code, exc.msg, exc.headers, exc.fp)
        self.retry_after = retry_after


class RateLimiter:
    """Enforce a minimum interval between the start of successive requests.

    An interval of zero (the default) disables the limiter.

    """

    def __init__(self, interval=0.0):
        self.interval = float(interval)
        self.last_request = None
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            if self.interval > 0 and self.last_request is not None:
                delay = self.interval - (time.monotonic() - self.last_request)
                if delay > 0:
                    time.sleep(delay)
            self.last_request = time.monotonic()

    def slow_down(self):
        with self.lock:
            if self.interval > 0:
                self.interval = min(self.interval * 2, MAX_RATE_LIMIT_INTERVAL)


_rate_limiter = RateLimiter()


def set_rate_limit(interval):
    """Set the minimum interval, in seconds, between requests to the eBird API.

    The limit applies to all requests made by the process. Setting it to
    zero, the default, disables rate limiting. If the API responds with
    HTTP 429 Too Many Requests, the interval is doubled, up to a maximum
    of MAX_RATE_LIMIT_INTERVAL, for the rest of the process, or until the
    rate limit is set again.

    :param interval: the number of seconds between requests.
    :type interval: float

    """
    if interval < 0:
        raise ValueError("The rate limit interval cannot be negative")
    with _rate_limiter.lock:
        _rate_limiter.interval = float(interval)


def get_rate_limit():
    """Get the current minimum interval, in seconds, between requests.

    :return: the interval, which may have increased since it was set, if the
    eBird API responded with HTTP 429 Too Many Requests.
    :rtype: float

    """
    return _rate_limiter.interval


def get_retry_after(exc):
    """Get the number of seconds to wait from a Retry-After header.

    :param exc: the error raised for the HTTP 429 response.
    :type exc: HTTPError

    :return: the number of seconds to wait, or None if the header was not
    present or could not be parsed.
    :rtype: float | None

    """
    value = exc.headers.get("Retry-After") if exc.headers else None
    if not value:
        return None
    try:
        return max(float(value), 0.0)
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=dt.timezone.utc)
    return max((when - dt.datetime.now(dt.timezone.utc)).total_seconds(), 0.0)


_parameter_defaults = {
    "back": constants.DEFAULT_BACK,
    "cat": constants.DEFAULT_SPECIES_CATEGORY,
    "detail": constants.DEFAULT_DETAIL,
    "dist": constants.DEFAULT_DISTANCE,
    "groupNameLocale": constants.DEFAULT_LOCALE,
    "hotspot": constants.DEFAULT_HOTSPOTS_ONLY,
    "includeProvisional": constants.DEFAULT_PROVISIONAL,
    "sort": constants.DEFAULT_OBSERVATION_ORDER,
    "locale": constants.DEFAULT_LOCALE,
    "sppLocale": constants.DEFAULT_LOCALE,
    "maxObservations": constants.DEFAULT_MAX_OBSERVATIONS,
    "maxObservers": constants.DEFAULT_MAX_OBSERVERS,
    "maxVisits": constants.DEFAULT_MAX_CHECKLISTS,
    "rankedBy": constants.DEFAULT_TOP_100_RANK,
}

_parameter_map = {
    "maxObservations": "maxResults",
    "maxObservers": "maxResults",
    "maxVisits": "maxResults",
}


def map_parameters(params):
    """Translate the names of the query parameters to match those used
    in the API.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    mapped = {}

    for key, value in params.items():
        key = _parameter_map.get(key, key)
        mapped[key] = value

    return mapped


def filter_parameters(params):
    """Filter out any parameter which matches the eBird API default value.

    :param params: a dict contains the GET parameters for the request that
    will be sent to the eBird API.

    :return: a copy of the params dictionary with only the parameters
    that are not set to a default value.

    """
    filtered = {}

    defaults = _parameter_defaults.copy()

    for key, value in params.items():
        if key in defaults:
            if value != defaults[key]:
                filtered[key] = value
        else:
            filtered[key] = value

    return filtered


def get_response(url, params=None, headers=None, max_retries=3, backoff_factor=1.0):
    """Get the content from the eBird API.

    :param url: the URL for the API call.
    :type url: str

    :param params: the query parameters for the API call.
    :type params: dict

    :param headers: the headers to add to the request.
    :type headers: dict

    :param max_retries: number of times to retry after an error response.
    :type max_retries: int

    :param backoff_factor: seconds to wait before the first retry; doubles
    on each subsequent attempt.
    :type backoff_factor: float

    :return: the content returned by the API
    :rtype: str

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises RateLimitError if the eBird API still returns HTTP 429 Too Many
    Requests after all the retries have been used.

    :raises HTTPError if the eBird API returns an error.

    """
    if params:
        url += "?" + urlencode(params, doseq=True)

    request = Request(url)

    if headers:
        for name, value in headers.items():
            request.add_header(name, value)

    for attempt in range(max_retries + 1):
        _rate_limiter.wait()
        try:
            return urlopen(request).read()
        except HTTPError as exc:
            retry_after = None
            if exc.code == 429:
                retry_after = get_retry_after(exc)
                _rate_limiter.slow_down()
                if attempt == max_retries:
                    raise RateLimitError(exc, retry_after) from exc
            elif attempt == max_retries:
                raise
            if retry_after is None:
                retry_after = backoff_factor * (2**attempt)
            time.sleep(retry_after)


def get_json(content):
    """Decode the JSON records from the response.

    :param content: the content returned by the eBird API.
    :type content: http.client.HTTPResponse:

    :return: the records decoded from the JSON payload.
    :rtype: list

    """
    return json.loads(content.decode("utf-8"))


def save_json(filename, data, indent=None):
    """Save results to a file.

    :param filename: the name of the file to save. The .json
    extension will be added if not present.

    :param data: the list of records to save.

    :param indent: whether to pretty-print results by adding indentation
    for each level. The default is no formatting.

    """
    if not filename.endswith(".json"):
        filename += ".json"
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=indent)


def call(url, params, headers, max_retries=3, backoff_factor=1.0):
    """Call the eBird API.

    :param url: the URL for the API call.
    :type url: str

    :param params: the query parameters for the API call.
    :type params: dict

    :param headers: the headers to add to the request.
    :type headers: dict

    :param max_retries: number of times to retry after an error response.
    :type max_retries: int

    :param backoff_factor: seconds to wait before the first retry; doubles
    on each subsequent attempt.
    :type backoff_factor: float

    :return: the content returned by the API
    :rtype: dict | list

    :raises URLError if there is an error with the connection to the
    eBird site.

    :raises HTTPError if the eBird API returns an error.

    :raises JSONDecodeError if the JSON data returned by the API is invalid.

    """
    filtered = filter_parameters(params)
    mapped = map_parameters(filtered)
    return get_json(
        get_response(
            url, mapped, headers, max_retries=max_retries, backoff_factor=backoff_factor
        )
    )
