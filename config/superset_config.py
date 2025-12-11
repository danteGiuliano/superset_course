import os
import logging
from cachelib.redis import RedisCache
from celery.schedules import crontab
from datetime import timedelta

# ================================
# Google Sheets (Shillelagh)
# ================================
# Ruta al archivo JSON del service account
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/gsheets-service-account.json"

# ======================================================
# Ejecutores de reportes
# ======================================================

# ======================================================
# Logging de librerías ruidosas
# ======================================================
logging.getLogger("paramiko").setLevel(logging.WARNING)

# ======================================================
# Feature Flags
# ======================================================
FEATURE_FLAGS = {
    "SHILLELAGH" : True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "EMBEDDED_SUPERSET": True,
    "SSH_TUNNELING": True,
    "ENABLE_FILE_UPLOAD": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "ENABLE_REACT_CRUD_VIEWS": True,
    "DASHBOARD_RBAC": True,
    "ENABLE_SCHEDULED_EMAIL_REPORTS": True,
    "ALERT_REPORTS": True,
    "THUMBNAILS": True,
    "ENABLE_GLOBAL_SEARCH": True,
    "ENABLE_EXPLORE_DRAG_AND_DROP": True,
    "ENABLE_DATA_EXPORT": True,
    "ENABLE_SQL_LAB_IMPROVEMENTS": True,
    "ENABLE_CUSTOM_METRICS": True,
    "ENABLE_ANNOTATIONS": True,
    "ENABLE_QUERY_CACHING": True,
    "EMAIL_NOTIFICATIONS": True,
    "ALERT_REPORTS_NOTIFICATION_DRY_RUN": False,  # CAMBIADO: debe ser False en producción
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS_SET": True,
    "DRILL_BY": True,
    "DYNAMIC_PLUGINS": True,
    "HORIZONTAL_FILTER_BAR": True,
    "ENABLE_TIME_SERIES_FORECAST2": True,
    "ALLOW_GUEST_TOKEN_JINJA_CONTEXT": True,
    "ENABLE_EXPLORE_JSON_CSRF": True,
    "ENABLE_SIP_34_METADATA_FIX": True,
    "SCHEDULED_QUERIES": True,
    "VERSIONED_EXPORT" : True,
    "TEMPLATE_PROCESSING_JINJA": True,
    "TAGGING_SYSTEM" : True
}

# ======================================================
# Webdriver para screenshots (Optimizado para v6)
# ======================================================
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--headless=new",  # Nuevo modo headless de Chrome
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-setuid-sandbox",
    "--disable-extensions",
    "--disable-software-rasterizer",
    "--disable-background-networking",
    "--disable-default-apps",
    "--disable-sync",
    "--disable-translate",
    "--hide-scrollbars",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--ignore-certificate-errors",
    "--ignore-ssl-errors",
    "--disable-blink-features=AutomationControlled",
    "--window-size=1920,1080",
    "--force-device-scale-factor=1",
]
WEBDRIVER_BASEURL = "http://superset_web:8088"

# CORREGIDO: usa variables de entorno para credenciales
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
REPORTS_WEBDRIVER_BASEURL = f"http://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@superset_web:8088"

# Este es el link que recibirá el usuario en el email
WEBDRIVER_BASEURL_USER_FRIENDLY = os.getenv("WEBDRIVER_BASEURL_USER_FRIENDLY", "http://localhost:8088")

# Timeouts optimizados
SCREENSHOT_LOCATE_WAIT = 30
SCREENSHOT_LOAD_WAIT = 90
WEBDRIVER_WAIT_TIME = 90

# Intervalos mínimos para reportes (descomenta si necesitas ajustar)
# ALERT_MINIMUM_INTERVAL = int(timedelta(minutes=10).total_seconds())
# REPORT_MINIMUM_INTERVAL = int(timedelta(minutes=5).total_seconds())

# ======================================================
# Mapbox
# ======================================================
MAPBOX_API_KEY = "pk.eyJ1IjoiZGdpdWxpYW5vMjciLCJhIjoiY21kaGRlYXRuMDBqZDJqcG1ycnh5ZzAwdiJ9.hopJfYyjRfHgSNQY1rj6fA"

# ======================================================
# Branding
# ======================================================
APP_NAME = "Indicadores"
FAVICON = "/static/assets/favicon.ico"
BRAND_COLOR = "#FF5733"

# ======================================================
# SMTP Email - CORREGIDO: usar variables de entorno
# ======================================================
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_MAIL_FROM = os.getenv("SMTP_MAIL_FROM", "")

# Configuración de seguridad SMTP
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() == "true"
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "False").lower() == "true"
SMTP_STARTTLS = SMTP_USE_TLS
SMTP_SSL_SERVER_AUTH = False

EMAIL_NOTIFICATIONS_TIMEOUT = 120
EMAIL_REPORTS_SUBJECT_PREFIX = "[Superset] "

# ======================================================
# Base de datos - CORREGIDO: usar variable de entorno
# ======================================================
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "superset")
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://superset:{POSTGRES_PASSWORD}@db:5432/superset"

# ======================================================
# Redis
# ======================================================
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# ======================================================
# Backends de cache y resultados
# ======================================================
RESULTS_BACKEND = RedisCache(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    key_prefix="superset_results_backend_"
)

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": int(REDIS_PORT),
    "CACHE_REDIS_DB": 1,
    "CACHE_REDIS_URL": f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
}

DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 86400,  # 1 día
    "CACHE_KEY_PREFIX": "sqlalchemy_",
    "CACHE_REDIS_URL": f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
}

FILTER_STATE_CACHE_CONFIG = {**CACHE_CONFIG, "CACHE_KEY_PREFIX": "superset_filter_"}
EXPLORE_FORM_DATA_CACHE_CONFIG = {**CACHE_CONFIG, "CACHE_KEY_PREFIX": "superset_explore_form_"}

# ======================================================
# Celery Config
# ======================================================
class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    imports = (
        "superset.sql_lab",
        "superset.tasks.scheduler",
    )
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    worker_prefetch_multiplier = 1  # CAMBIADO: reduce prefetch para evitar bloqueos
    task_acks_late = True
    task_annotations = {
        "sql_lab.get_sql_results": {
            "rate_limit": "100/s",
        },
        "reports.execute": {
            "time_limit": 600,  # 10 minutos timeout
            "soft_time_limit": 540,  # 9 minutos soft timeout
        },
    }
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),  # Cada minuto
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=0, hour=0),  # Diariamente a medianoche
        },
    }

CELERY_CONFIG = CeleryConfig

# ======================================================
# Límites de tiempo - AUMENTADOS para reportes
# ======================================================
SQLLAB_ASYNC_TIME_LIMIT_SEC = 60 * 60
SUPERSET_WEBSERVER_TIMEOUT = 60 * 10  # 10 minutos
CELERYD_TASK_TIME_LIMIT = 60 * 10  # 10 minutos para tasks de Celery

# ======================================================
# File Upload
# ======================================================
UPLOAD_FOLDER = "/app"
ALLOWED_FILE_UPLOAD_EXTENSIONS = [".csv", ".xls", ".xlsx"]
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB

# ======================================================
# Seguridad y proxy - CORREGIDO: usar variable de entorno
# ======================================================
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "CHANGE_THIS_SECRET_KEY")
DEBUG = False
FLASK_ENV = "production"
ENABLE_PROXY_FIX = True
PROXY_FIX_CONFIG = {"x_for": 1, "x_proto": 1, "x_host": 1, "x_port": 0, "x_prefix": 1}

# ======================================================
# CORS
# ======================================================
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "expose_headers": ["*"],
    "origins": ["*"],
}

# ======================================================
# i18n
# ======================================================
BABEL_DEFAULT_LOCALE = "es"
LANGUAGES = {
    "es": {"flag": "es", "name": "Español"},
    "en": {"flag": "us", "name": "English"},
}

# ======================================================
# Visualización numérica
# ======================================================
D3_FORMAT = {
    "decimal": ",",
    "thousands": ".",
    "currency": ["$", ""],
    "grouping": [3],
}

# ======================================================
# Rate limiting
# ======================================================
RATELIMIT_STORAGE_URI = REDIS_URL

# ======================================================
# CSP (deshabilitado en dev, habilitar en prod)
# ======================================================
CONTENT_SECURITY_POLICY_WARNING = False
TALISMAN_ENABLED = False

# ======================================================
# Logging para debugging de emails (opcional)
# ======================================================
# import logging
# logging.getLogger('superset.tasks.scheduler').setLevel(logging.DEBUG)
# logging.getLogger('superset.reports').setLevel(logging.DEBUG)