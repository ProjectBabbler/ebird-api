from io import BytesIO
from unittest import TestCase
from unittest.mock import MagicMock, call, patch
from urllib.error import HTTPError

from ebird.api.requests.utils import get_response


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
