from .base import *  # noqa
from .base import env

import os


# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = "9f43d31e_s#)&)j-^zjz(tgwr4yj1y=npy!tz$(-&#=w8a=g7l"

# SECURITY WARNING: don't run with debug turned on in production!
READ_DOT_ENV_FILE = True
DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]


# CORS
CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)

# EMAIL
# ------------------------------------------------------------------------------

# # https://docs.djangoproject.com/en/dev/ref/settings/#email-host
# EMAIL_HOST = "localhost"
# # https://docs.djangoproject.com/en/dev/ref/settings/#email-port
# EMAIL_PORT = 1025
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# DATABASES
# ------------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    # {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (
    "rest_framework.renderers.BrowsableAPIRenderer",
)

# ------------------------------------------------------------------------------

# Vue router in hash(default) mode
# FRONTEND_URL = "http://127.0.0.1:8000/#/"

# Vue router in history mode
FRONTEND_URL = "http://localhost:3000/"

# ACCOUNT_EMAIL_CONFIRMATION_URL = FRONTEND_URL + 'verify-email/{}'
ACCOUNT_PASSWORD_RESET_CONFIRM = FRONTEND_URL + "password/reset/confirm/"


# media
# ------------------------------------------------------------------------------
# MEDIA_URL = "127.0.0.1:8000/media/"
