import os
from pathlib import Path

# Project root = folder containing this config.py
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)  # ensure folder exists


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret-key'
    SECURITY_PASSWORD_SALT = 'salt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SECURITY_CSRF_PROTECT_MECHANISMS = []
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_SEND_RESPONSE_BEHAVIOR = 'json'
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = False
    # SECURITY_USER_IDENTITY_ATTRIBUTES = ('username', )
    SECURITY_USERNAME_ENABLE = True
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # Mail configuration (using a placeholder/local server by default)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 1025))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "glowsuite8@gmail.com")

    # Scheduler Configuration
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'job1',
            'func': 'application.tasks:daily_notification_cleanup',
            'trigger': 'interval',
            'seconds': 3600  # Run every hour
        },
        {
            'id': 'job2',
            'func': 'application.tasks:send_daily_reminder',
            'trigger': 'cron',
            'hour': 9,
            'minute': 0  # Run every day at 9:00 AM
        },
        {
            'id': 'attendance_threshold_job',
            'func': 'application.tasks:mark_absent_staff',
            'trigger': 'cron',
            'hour': 19,
            'minute': 31 # Placeholder: 12:01 PM
        },
        {
            'id': 'daily_birthday_job',
            'func': 'application.tasks:check_daily_birthdays',
            'trigger': 'cron',
            'hour': 19,
            'minute': 43    
        }
    ]


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{(INSTANCE_DIR / 'sm_devdb.db').as_posix()}"
