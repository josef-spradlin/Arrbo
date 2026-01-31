import os

API_BASE_URL = os.getenv("ARRBO_API_BASE_URL", "http://localhost:8080")
HTTP_TIMEOUT_S = float(os.getenv("ARRBO_HTTP_TIMEOUT", "10"))
