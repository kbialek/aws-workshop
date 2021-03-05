#!/usr/bin/bash -xe
export FLASK_CONFIG=prod

# Export current EC2 instance-id into env variable
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
export INSTANCE_ID

# Load DB credentials into env variables
source ../env.sh

# Download RDS CA certificate
wget https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem

# Upgrade DB Schema
export FLASK_APP=run.py
flask db upgrade

/usr/local/bin/gunicorn \
  -w 4 \
  --log-file /var/log/demo-app.log \
  --statsd-host 127.0.0.1:8125 \
  -b 0.0.0.0:8080 \
  run:app
