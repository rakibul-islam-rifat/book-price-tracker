import logging
import time
from functools import wraps

import requests

logger = logging.getLogger(__name__)
my_header: dict = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def add_delay(delay=2):
    """Decorator to enforce a minimum delay between function calls."""

    def decorator(func):
        last_called = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_called

            if last_called is not None:
                elapsed = time.time() - last_called

                if elapsed < delay:
                    wait = delay - elapsed

                    logger.info("waiting %.2fs before next request ...", wait)
                    time.sleep(wait)

            result = func(*args, **kwargs)
            last_called = time.time()
            return result

        return wrapper

    return decorator


def _handle_retry(attempt, error_msg, wait_seconds):
    logger.warning("Attempt %d — %s, waiting %ds...", attempt, error_msg, wait_seconds)
    time.sleep(wait_seconds)


@add_delay(delay=3)
def fetch_url(
    url: str,
    headers: dict = my_header,
    payload: dict | None = None,
    max_attempts: int = 3,
) -> requests.Response:
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            response: requests.Response = requests.get(
                url, headers=headers, params=payload, timeout=10
            )
            response.raise_for_status()
            response.encoding = "utf-8"
            return response

        except requests.exceptions.Timeout as e:
            last_error = e
            _handle_retry(attempt, "timed out", 2)

        except requests.exceptions.ConnectionError as e:
            last_error = e
            _handle_retry(attempt, "connection error", 2**attempt)

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            if status_code and (status_code == 429 or status_code >= 500):
                last_error = e
                _handle_retry(attempt, f"server error {status_code}", 2)
            else:
                raise

    logger.error("All %d attempts failed. Last Error: %s", max_attempts, last_error)
    raise RuntimeError(f"All {max_attempts} attempts failed. Last error: {last_error}")
