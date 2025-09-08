from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 SECURITY
SECRET_KEY = 'django-insecure-h_m^romijy+4$4ms3o9gsehrwg7l(2j+b98h*58%ka4$1vh1=('
DEBUG = True
ALLOWED_HOSTS = ["*"]   # in production replace with domain/ip

# 🚀 Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'channels',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # Local
    'api',
    'payments'
]

ASGI_APPLICATION = "api.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# 🌍 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',   # allow frontend requests
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iecapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'iecapi.wsgi.application'

# 💾 Database (for now SQLite, can switch to PostgreSQL later)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔑 Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌐 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 📂 Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# 🔧 DRF + JWT Settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', # for browsable API login
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# 🔐 Custom user
AUTH_USER_MODEL = 'api.User'

# 🌍 CORS (to allow frontend React/Vercel)
CORS_ALLOW_ALL_ORIGINS = True   # for dev only; in prod use whitelist
# Example: CORS_ALLOWED_ORIGINS = ["https://nexus-iota-five.vercel.app"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Stripe keys
# STRIPE_SECRET_KEY = "sk_test_51S1mBPJz1wMP4h7RZClf0M6MfFMjL8RXcgTB06s25wBnVXXAGNzRESsxpmGkYIkQohMy0NRyUlMDdahElJRYhOo200MOBZrEy0"
# STRIPE_PUBLISHABLE_KEY = "pk_test_51S1mBPJz1wMP4h7RRS5XpVkuSSzn5zabWZz5yBEHZfzx9zfBxPBvxiEFmjm0ECqzPOsgQGvGUZPA8hMjw9gZvJtj00IdoyQd3j"



SPECTACULAR_SETTINGS = {
    "TITLE": "IEC API",
    "DESCRIPTION": "API for IEC Internship Project with Authentication, Meetings (WebRTC), and Payments",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
