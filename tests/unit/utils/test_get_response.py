import datetime as dt
from email.utils import format_datetime
from io import BytesIO
from unittest import TestCase
from unittest.mock import MagicMock, call, patch
from urllib.error import HTTPError

from ebird.api.requests import utils
from ebird.api.requests.utils import (
    MAX_RATE_LIMIT_INTERVAL,
    RateLimitError,
    get_rate_limit,
    get_response,
    get_retry_after,
    set_rate_limit,
)


def make_error(code, retry_after=None):
    headers = MagicMock()
    headers.get.return_value = retry_after
    return HTTPError("http://example.com", code, "Error", headers, BytesIO(b""))


def make_response(content=b"[]"):
    response = MagicMock()
    response.read.return_value = content
    return response


class GetResponseRetryTests(TestCase):
    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_no_retry_on_success(self, mock_urlopen, mock_sleep):
        mock_urlopen.return_value = make_response()
        get_response("http://example.com", max_retries=3)
        mock_sleep.assert_not_called()

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_retries_on_http_error(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = [make_error(500), make_response()]
        get_response("http://example.com", max_retries=3, backoff_factor=1.0)
        mock_sleep.assert_called_once_with(1.0)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_raises_after_max_retries_exhausted(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = make_error(500)
        with self.assertRaises(HTTPError):
            get_response("http://example.com", max_retries=2, backoff_factor=1.0)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_exponential_backoff(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = [make_error(500), make_error(500), make_response()]
        get_response("http://example.com", max_retries=3, backoff_factor=2.0)
        self.assertEqual(mock_sleep.call_args_list, [call(2.0), call(4.0)])

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_429_uses_retry_after_header(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = [make_error(429, retry_after="30"), make_response()]
        get_response("http://example.com", max_retries=3)
        mock_sleep.assert_called_once_with(30.0)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_429_without_retry_after_uses_backoff(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = [make_error(429, retry_after=None), make_response()]
        get_response("http://example.com", max_retries=3, backoff_factor=1.0)
        mock_sleep.assert_called_once_with(1.0)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_non_429_ignores_retry_after_header(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = [make_error(500, retry_after="30"), make_response()]
        get_response("http://example.com", max_retries=3, backoff_factor=1.0)
        mock_sleep.assert_called_once_with(1.0)


class GetResponseRateLimitErrorTests(TestCase):
    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_raises_rate_limit_error_after_retries_exhausted(
        self, mock_urlopen, mock_sleep
    ):
        mock_urlopen.side_effect = make_error(429, retry_after="30")
        with self.assertRaises(RateLimitError) as context:
            get_response("http://example.com", max_retries=1)
        self.assertEqual(context.exception.retry_after, 30.0)
        self.assertEqual(context.exception.code, 429)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_rate_limit_error_is_http_error(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = make_error(429)
        with self.assertRaises(HTTPError):
            get_response("http://example.com", max_retries=0)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_other_errors_are_not_rate_limit_errors(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = make_error(500)
        with self.assertRaises(HTTPError) as context:
            get_response("http://example.com", max_retries=0)
        self.assertNotIsInstance(context.exception, RateLimitError)


class GetRetryAfterTests(TestCase):
    def test_seconds(self):
        self.assertEqual(get_retry_after(make_error(429, retry_after="5")), 5.0)

    def test_missing(self):
        self.assertIsNone(get_retry_after(make_error(429, retry_after=None)))

    def test_http_date(self):
        when = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=120)
        value = format_datetime(when, usegmt=True)
        delay = get_retry_after(make_error(429, retry_after=value))
        self.assertTrue(110 < delay <= 120)

    def test_http_date_in_past(self):
        value = "Wed, 21 Oct 2015 07:28:00 GMT"
        self.assertEqual(get_retry_after(make_error(429, retry_after=value)), 0.0)

    def test_invalid(self):
        self.assertIsNone(get_retry_after(make_error(429, retry_after="soon")))


class RateLimitTests(TestCase):
    def setUp(self):
        utils._rate_limiter.last_request = None

    def tearDown(self):
        set_rate_limit(0)

    def test_disabled_by_default(self):
        self.assertEqual(get_rate_limit(), 0.0)

    def test_negative_interval_raises(self):
        with self.assertRaises(ValueError):
            set_rate_limit(-1)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.time.monotonic")
    @patch("ebird.api.requests.utils.urlopen")
    def test_waits_between_requests(self, mock_urlopen, mock_monotonic, mock_sleep):
        set_rate_limit(2.0)
        mock_urlopen.return_value = make_response()
        # first request at t=100, second starts at t=100.5
        mock_monotonic.side_effect = [100.0, 100.5, 102.0]
        get_response("http://example.com")
        get_response("http://example.com")
        mock_sleep.assert_called_once_with(1.5)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.time.monotonic")
    @patch("ebird.api.requests.utils.urlopen")
    def test_no_wait_if_interval_elapsed(
        self, mock_urlopen, mock_monotonic, mock_sleep
    ):
        set_rate_limit(2.0)
        mock_urlopen.return_value = make_response()
        mock_monotonic.side_effect = [100.0, 103.0, 103.0]
        get_response("http://example.com")
        get_response("http://example.com")
        mock_sleep.assert_not_called()

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_429_doubles_interval(self, mock_urlopen, mock_sleep):
        set_rate_limit(1.0)
        mock_urlopen.side_effect = [make_error(429), make_response()]
        get_response("http://example.com", max_retries=1)
        self.assertEqual(get_rate_limit(), 2.0)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_interval_is_capped(self, mock_urlopen, mock_sleep):
        set_rate_limit(MAX_RATE_LIMIT_INTERVAL)
        mock_urlopen.side_effect = [make_error(429), make_response()]
        get_response("http://example.com", max_retries=1)
        self.assertEqual(get_rate_limit(), MAX_RATE_LIMIT_INTERVAL)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_429_does_not_enable_disabled_limiter(self, mock_urlopen, mock_sleep):
        mock_urlopen.side_effect = [make_error(429), make_response()]
        get_response("http://example.com", max_retries=1)
        self.assertEqual(get_rate_limit(), 0.0)

    @patch("ebird.api.requests.utils.time.sleep")
    @patch("ebird.api.requests.utils.urlopen")
    def test_other_errors_do_not_change_interval(self, mock_urlopen, mock_sleep):
        set_rate_limit(1.0)
        mock_urlopen.side_effect = [make_error(500), make_response()]
        get_response("http://example.com", max_retries=1)
        self.assertEqual(get_rate_limit(), 1.0)
