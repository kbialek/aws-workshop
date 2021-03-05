import json
import pymysql
import boto3
import cfnresponse


def lambda_handler(event, context):
    # Log event to simplify troubleshooting
    print(event)

    # Request type can be either: Create, Update or Delete
    request_type = event['RequestType']

    # CFN request types other than Create do nothing
    if request_type != 'Create':
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        return

    props = event['ResourceProperties']
    aws_region = props['AwsRegion']
    sa_secret_name = props['SaSecretName']
    app_secret_name = props['AppSecretName']

    try:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=aws_region)

        # Read sa user secret from SecretsManager
        sa_secret = json.loads(client.get_secret_value(SecretId=sa_secret_name)['SecretString'])
        app_secret = json.loads(client.get_secret_value(SecretId=app_secret_name)['SecretString'])

        # Connect to the database engine
        conn = pymysql.connect(
            host=sa_secret['host'],
            user=sa_secret['username'],
            passwd=sa_secret['password'],
            db='mysql',
            connect_timeout=5
        )

        # Create database objects
        try:
            with conn.cursor() as cur:
                cur.execute("create database aws_workshop")
                cur.execute("create user demo_app@'%' identified by '{}'".format(app_secret['password']))
                cur.execute("grant all on aws_workshop.* to demo_app@'%'")
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        finally:
            conn.close()

    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {
            'exception': str(e)
        })
