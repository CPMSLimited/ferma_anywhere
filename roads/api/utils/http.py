import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def build_retrying_session(
    total=3,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset(["GET"]),
    timeout=8,
):
    """
    Returns a requests.Session configured with retries and sane timeouts.
    """
    session = requests.Session()

    retry = Retry(
        total=total,
        read=total,
        connect=total,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=allowed_methods,
        raise_on_status=False,
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # attach a default timeout to session.get via a small wrapper
    original_get = session.get
    def get_with_timeout(*args, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = timeout
        return original_get(*args, **kwargs)
    session.get = get_with_timeout

    return session
