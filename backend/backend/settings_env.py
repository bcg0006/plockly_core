"""
Environment-specific Django settings configuration.
This file handles different settings for development, staging, and production.
"""

import os
from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-this-in-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

# Environment detection
ENVIRONMENT = config("ENVIRONMENT", default="development")

# Allowed hosts configuration
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="plockly"),
        "USER": config("POSTGRES_USER", default="postgres"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="postgres"),
        "HOST": config("POSTGRES_HOST", default="localhost"),
        "PORT": config("POSTGRES_PORT", default="5432", cast=int),
    }
}

# Redis configuration
REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/0")

# CORS configuration
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://localhost:3001",
    cast=Csv(),
)

# Email configuration
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default=25, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

# Security settings based on environment
if ENVIRONMENT == "production":
    # Production security settings
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
    CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
    SECURE_BROWSER_XSS_FILTER = config(
        "SECURE_BROWSER_XSS_FILTER", default=True, cast=bool
    )
    SECURE_CONTENT_TYPE_NOSNIFF = config(
        "SECURE_CONTENT_TYPE_NOSNIFF", default=True, cast=bool
    )
    SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True, cast=bool
    )
    SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=True, cast=bool)
else:
    # Development/Staging security settings
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
    SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
    CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
    SECURE_BROWSER_XSS_FILTER = config(
        "SECURE_BROWSER_XSS_FILTER", default=True, cast=bool
    )
    SECURE_CONTENT_TYPE_NOSNIFF = config(
        "SECURE_CONTENT_TYPE_NOSNIFF", default=True, cast=bool
    )

# Logging configuration
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOG_FILE = config("LOG_FILE", default="")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

# Add file logging if LOG_FILE is specified
if LOG_FILE:
    LOGGING["handlers"]["file"] = {
        "class": "logging.FileHandler",
        "filename": LOG_FILE,
        "formatter": "verbose",
    }
    LOGGING["root"]["handlers"].append("file")

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Session configuration
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# JWT settings with environment-specific overrides
JWT_ACCESS_TOKEN_LIFETIME = config("JWT_ACCESS_TOKEN_LIFETIME", default=15, cast=int)
JWT_REFRESH_TOKEN_LIFETIME = config("JWT_REFRESH_TOKEN_LIFETIME", default=7, cast=int)

# Monitoring and analytics
SENTRY_DSN = config("SENTRY_DSN", default="")
GOOGLE_ANALYTICS_ID = config("GOOGLE_ANALYTICS_ID", default="")
HEALTH_CHECK_ENABLED = config("HEALTH_CHECK_ENABLED", default=True, cast=bool)

# Performance settings
CACHE_TIMEOUT = config("CACHE_TIMEOUT", default=300, cast=int)
SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", default=1209600, cast=int)
