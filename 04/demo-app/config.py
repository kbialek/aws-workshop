import os
import boto3


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    SQLALCHEMY_TRACK_MODIFICATIONS = []


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:fireup@localhost/aws_workshop'


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    aws_region = os.getenv('AWS_REGION')
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    if db_password is None and aws_region:
        rds_client = boto3.client('rds', region_name=aws_region)
        db_password = rds_client.generate_db_auth_token(db_host, 3306, db_user)

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{host}/aws_workshop'.format(host=db_host)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'user': db_user,
            'passwd': db_password,
            'ssl_ca': 'rds-ca-2019-root.pem'
        }
    }


app_config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
