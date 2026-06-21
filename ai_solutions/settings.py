"""Django settings for the AI-Solution website."""
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-ai-solution-local-development-key",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "website",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ai_solutions.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "website.context_processors.site_settings",
                "website.context_processors.admin_dashboard",
            ],
        },
    },
]

WSGI_APPLICATION = "ai_solutions.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "assets"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LUdbx3CvuzEauhot26OLUXdlGSFkSkME7fI2DWq5GH2Q")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEMO_ADMIN_EMAIL = os.environ.get("AI_SOLUTION_ADMIN_EMAIL", "admin@ai-solution.example")
DEMO_ADMIN_PASSWORD = os.environ.get("AI_SOLUTION_ADMIN_PASSWORD", "admin123")

JAZZMIN_SETTINGS = {
    "site_title": "AI-Solution Admin",
    "site_header": "AI-Solution",
    "site_brand": "AI-Solution",
    "site_logo": "img/logo-mark.svg",
    "welcome_sign": "AI-Solution management console",
    "copyright": "AI-Solution",
    "search_model": ["website.ContactInquiry", "website.Service", "website.Article", "auth.User"],
    "topmenu_links": [
        {"name": "Website", "url": "/", "new_window": True},
        {"model": "website.ContactInquiry"},
        {"app": "website"},
    ],
    "usermenu_links": [
        {"name": "Public website", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["website", "auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-shield",
        "auth.Group": "fas fa-users",
        "website": "fas fa-layer-group",
        "website.ContactInquiry": "fas fa-inbox",
        "website.SiteSetting": "fas fa-sliders-h",
        "website.PageContent": "fas fa-file-alt",
        "website.FeatureCard": "fas fa-th-large",
        "website.Metric": "fas fa-chart-line",
        "website.Service": "fas fa-concierge-bell",
        "website.PortfolioItem": "fas fa-briefcase",
        "website.Event": "fas fa-calendar-alt",
        "website.Article": "fas fa-newspaper",
        "website.Testimonial": "fas fa-star",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": "css/admin.css",
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    "navbar": "navbar-white navbar-light",
    "navbar_fixed": True,
    "no_navbar_border": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_fixed": True,
    "brand_colour": "navbar-teal",
    "accent": "accent-teal",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}
