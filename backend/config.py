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
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = False
    # SECURITY_USER_IDENTITY_ATTRIBUTES = ('username', )
    SECURITY_USERNAME_ENABLE = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{(INSTANCE_DIR / 'sm_devdb.db').as_posix()}"
