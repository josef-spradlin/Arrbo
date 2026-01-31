import requests
from qa.utils.config import API_BASE_URL, HTTP_TIMEOUT_S

def api_get(path: str, **kwargs) -> requests.Response:
    url = f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    return requests.get(url, timeout=HTTP_TIMEOUT_S, **kwargs)
