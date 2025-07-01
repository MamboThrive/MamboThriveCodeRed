from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zgtg)gph&8d8nf)kwq$1ls!h^ds&a_64a)tv4n5z#*7_0p26tz"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

NPM_BIN_PATH = "C:\\Program Files\\nodejs\\npm.cmd"

OPENROUTER_KEY = os.getenv('OPENROUTER_KEY', None)


try:
    from .local import *
except ImportError:
    pass
