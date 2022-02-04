import os

os_env = os.environ


class Config(object):
    SECRET_KEY = '3nF3Rn0'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""
    # app config
    ENV = 'prd'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = False

    # JWT Config
    JWT_SECRET_KEY = '1234567a@'

    # mysql config
    SQLALCHEMY_DATABASE_URI = 'mysql://admin:KnightZ191131@tdhv-db.cwrx1r2wwyzr.ap-southeast-1.rds.amazonaws.com/tdhv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # aws config
    S3_ENDPOINT = 'https://tdhv.s3.ap-southeast-1.amazonaws.com'
    AWS_REGION_NAME = 'ap-southeast-1'


class DevConfig(Config):
    """Staging configuration."""
    # app config
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = True

    # JWT Config
    JWT_SECRET_KEY = '1234567a@'

    # mysql config
    SQLALCHEMY_DATABASE_URI = 'mysql://admin:KnightZ191131@tdhv-db.cwrx1r2wwyzr.ap-southeast-1.rds.amazonaws.com/tdhv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # aws config
    S3_ENDPOINT = 'https://tdhv.s3.ap-southeast-1.amazonaws.com'
    AWS_REGION_NAME = 'ap-southeast-1'
