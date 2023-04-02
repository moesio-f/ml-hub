import os
from . import login

_JWT = [None]
_URL = os.environ.get('API_GATEWAY', 'http://localhost:8080')

del os
