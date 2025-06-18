from pathlib import Path
from datetime import timedelta
from decouple import config
import cloudinary
import os
import dj_database_url # Import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    'cloudinary',
    'cloudinary_storage',
    "django_filters",
    "Core",
    "Users",
    "Delivery",
    "Customers",
    "Payments",
    "Reports",
    "Notification",
    'search',
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    # "DATETIME_FORMAT": "%d/%m/%y %H:%M", # This line was commented out in your original code
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "BLACKLIST_AFTER_ROTATION": True,
    "ROTATE_REFRESH_TOKENS": True,
    "TOKEN_BLACKLIST_ENABLED": True,
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "POS_SYSTEM.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "POS_SYSTEM.wsgi.application"

# Database
# Use dj_database_url to parse the DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.parse(config("DATABASE_URL"), conn_max_age=600)
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AFRICASTALKING_USERNAME = config("AFRICASTALKING_USERNAME")
AFRICASTALKING_API_KEY = config("AFRICASTALKING_API_KEY")

CORS_ALLOWED_ORIGINS = config("ALLOWED_CORS_ORIGINS").split(",")