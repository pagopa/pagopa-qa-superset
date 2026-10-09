import os


FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
}

TALISMAN_ENABLED = False

ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "origins": [os.getenv('PAGOPA-QA-HUB-URL')],
}


GUEST_ROLE_NAME = "Public"
GUEST_TOKEN_HEADER_NAME = "X-GuestToken"

GUEST_TOKEN_JWT_EXP_SECONDS  = 3600 # 1 hour in seconds