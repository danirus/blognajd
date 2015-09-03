import imp
import os

PRJ_PATH = os.path.abspath(os.path.curdir)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ("Alice Bloggs", "alice@example.com"),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   "django.db.backends.sqlite3",
        'NAME':     "blognajd.db",
        'USER':     "",
        'PASSWORD': "", 
        'HOST':     "", 
        'PORT':     "",
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Europe/Brussels"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PRJ_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PRJ_PATH, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(PRJ_PATH, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = "/static/admin/"

SECRET_KEY = "v2824l&2-n+4zznbsk9c-ap5i)b3e8b+%*a=dxqlahm^%)68jn"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = "urls"

TEMPLATE_DIRS = (
    os.path.abspath(
        os.path.join(imp.find_module("blognajd")[1], "templates")),
)

try:
    import imp
    imp.find_module('django_comments')
    django_comments = 'django_comments'
except ImportError:
    django_comments = 'django.contrib.comments'

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    django_comments,
    "django.contrib.admin",

    "crispy_forms",
    "django_contactme",
    "django_comments_xtd",
    "django_markup",
    "inline_media",
    "flatblocks_xtd",
    "sorl.thumbnail",
    "classytags",
    "taggit",
    "taggit_templatetags2",
    "usersettings",
    "blognajd",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "blognajd.context_processors.settings",
)

#EMAIL_HOST          = "smtp.gmail.com" 
#EMAIL_PORT          = "587"
#EMAIL_HOST_USER     = ""
#EMAIL_HOST_PASSWORD = ""
#EMAIL_USE_TLS       = True # Yes for Gmail
DEFAULT_FROM_EMAIL  = "Alice Bloggs <alice@example.com>"
SERVER_EMAIL        = DEFAULT_FROM_EMAIL

# Fill in actual EMAIL settings above, and comment out the 
# following line to let this django demo sending emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

COMMENTS_APP = "django_comments_xtd"
COMMENTS_XTD_CONFIRM_EMAIL = True
COMMENTS_XTD_SALT = b"es-war-einmal-una-princesa-in-a-beautiful-castle"

THUMBNAIL_BACKEND = "inline_media.sorl_backends.AutoFormatBackend"
THUMBNAIL_FORMAT = "JPEG"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple' 
        },
        'sorl-thumbnail': {
            'level': 'ERROR',
            'class': 'sorl.thumbnail.log.ThumbnailLogHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'inline_media': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'sorl.thumbnail': {
            'handler': ['sorl-thumbnail'],
            'level': 'ERROR',
        }
    }
}

LOGIN_URL = "/"

CONTACTME_NOTIFY_TO = "Your Name <user@example.com>"
CONTACTME_SALT = b'change this, write random chars and special chars'

INLINE_MEDIA_TEXTAREA_ATTRS = {
    'default': {
        'style': 'font: 13px monospace'
    },
}

COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_CONFIRM_EMAIL = True
COMMENTS_XTD_FORM_CLASS = "blognajd.forms.CrispyXtdCommentForm"

TAGGIT_CASE_INSENSITIVE = True

USERSETTINGS_MODEL='blognajd.SiteSettings'

BLOGNAJD_THEMES_APP_STATIC_PATH = 'blognajd/themes'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
