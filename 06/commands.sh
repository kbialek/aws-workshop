#!/usr/bin/env bash
set -euf -o pipefail +o allexport

BACKEND_STACK_NAME="BackendStack"
FRONTEND_STACK_NAME="FrontendStack"
BUILD_STACK_NAME="BuildStack"
KEY_PAIR="kbialek"
WEBSITE_SSL_CERTIFICATE_ARN="arn:aws:acm:us-east-1:759483279519:certificate/893ce825-8a53-4bbf-8d71-238db5130f69"
API_SSL_CERTIFICATE_ARN="arn:aws:acm:eu-central-1:759483279519:certificate/ac0f18af-b0fc-4aea-aab7-bd5d4abda6f9"

### Build Stack

function deploy-build-stack() {
    template_file="build-template-$2.yaml"
    aws cloudformation deploy \
      --stack-name "$BUILD_STACK_NAME" \
      --template-file "$template_file" \
      --capabilities CAPABILITY_IAM
}

function delete-build-stack() {
    BUCKET=$(get-deployment-bucket)
    aws s3 rm --recursive "s3://$BUCKET/"
    aws cloudformation delete-stack --stack-name "$BUILD_STACK_NAME"
}

function get-deployment-bucket() {
    aws cloudformation describe-stacks \
      --stack-name "$BUILD_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='DeploymentBucket'].OutputValue" \
      --output text
}

## Backend

function app-backend-package() {
    rm -f demo-app.zip
    cd demo-app/backend
    zip -r ../../upload/demo-app.zip . -x \*__pycache__*
    cd -
}

function app-backend-upload() {
  BUCKET=$(get-deployment-bucket)
  aws s3 cp upload/demo-app.zip "s3://$BUCKET/"
}

## Frontend

function app-frontend-package() {
    cd demo-app/frontend
    yarn build
    cd -
}

function deploy-frontend-stack() {
    template_file="frontend-template-$2.yaml"
    aws cloudformation deploy \
      --stack-name "$FRONTEND_STACK_NAME" \
      --template-file "$template_file" \
      --capabilities CAPABILITY_IAM \
      --parameter-overrides \
        SslCertificateArn="$WEBSITE_SSL_CERTIFICATE_ARN"
}

function get-website-bucket() {
    aws cloudformation describe-stacks \
      --stack-name "$FRONTEND_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='WebsiteBucket'].OutputValue" \
      --output text
}

function get-website-cloudfront-bucket() {
    aws cloudformation describe-stacks \
      --stack-name "$FRONTEND_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='WebsiteCloudfrontBucket'].OutputValue" \
      --output text
}

function get-website-domain-name() {
    aws cloudformation describe-stacks \
      --stack-name "$FRONTEND_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='WebsiteDomainName'].OutputValue" \
      --output text
}

function app-frontend-upload() {
    WEBSITE_BUCKET="$(get-website-bucket)"
    aws s3 sync --delete --acl public-read demo-app/frontend/build/ "s3://$WEBSITE_BUCKET"
    WEBSITE_CLOUDFRONT_BUCKET="$(get-website-cloudfront-bucket)"
    aws s3 sync --delete demo-app/frontend/build/ "s3://$WEBSITE_CLOUDFRONT_BUCKET"
}

## Lambdas

function app-lambda-package() {
    base_dir=$(pwd)
    upload_dir="$base_dir/upload"
    lambda_name="$2"
    lambda_dir="demo-app/lambda/$lambda_name"
    zip_file="$upload_dir/$lambda_name.zip"
    rm "$zip_file"
    cd "$lambda_dir"
    # install and package requirements
    mkdir -p package
    pip3 install --target ./package -r requirements.txt
    cd package
    zip -r "$zip_file" . -x \*__pycache__*
    cd -
    # package function code
    zip -g -r "$zip_file" . -x \*__pycache__* -x \package/*
    cd "$base_dir"
}

function app-lambda-upload() {
  BUCKET=$(get-deployment-bucket)
  aws s3 cp --recursive upload/ "s3://$BUCKET/lambda"
}

### Application Stack

function deploy-stack() {
    template_file="template-$2.yaml"
    DEPLOYMENT_BUCKET=$(get-deployment-bucket)
    aws cloudformation deploy \
      --stack-name "$BACKEND_STACK_NAME" \
      --template-file "$template_file" \
      --capabilities CAPABILITY_IAM \
      --parameter-overrides \
        KeyPair="$KEY_PAIR" \
        DeploymentBucket="$DEPLOYMENT_BUCKET" \
        ApiSslCertificate="$API_SSL_CERTIFICATE_ARN"
}

function delete-stack() {
    LOGS_BUCKET_NAME=$(get-logs-bucket)
    aws s3 rm --recursive "s3://$LOGS_BUCKET_NAME"
    aws cloudformation delete-stack --stack-name "$BACKEND_STACK_NAME"
}

function get-logs-bucket() {
    aws cloudformation describe-stacks \
      --stack-name "$BACKEND_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='LogsBucket'].OutputValue" \
      --output text
}

function get-asg-ec2-public-ip() {
    ASG_NAME=$(aws cloudformation describe-stacks \
      --stack-name "$BACKEND_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='AsgName'].OutputValue" \
      --output text)
    INSTANCES=$(aws autoscaling describe-auto-scaling-groups \
      --auto-scaling-group-names "$ASG_NAME" \
      --query "AutoScalingGroups[0].Instances[?LifecycleState=='InService'].InstanceId" \
      --output text)
    aws ec2 describe-instances \
      --instance-ids $INSTANCES \
      --query "Reservations[].Instances[].PublicIpAddress" \
      --output text
}

$1 "$@"
