#!/usr/bin/env bash
set -euf -o pipefail +o allexport

APP_STACK_NAME="AppStack"
BUILD_STACK_NAME="BuildStack"
KEY_PAIR="kbialek"

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

function app-package() {
    rm -f demo-app.zip
    cd demo-app
    zip -r ../demo-app.zip . -x \*__pycache__*
    cd -
}

function app-upload() {
  BUCKET=$(get-deployment-bucket)
  aws s3 cp demo-app.zip "s3://$BUCKET/"
}

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
      --stack-name "$APP_STACK_NAME" \
      --template-file "$template_file" \
      --capabilities CAPABILITY_IAM \
      --parameter-overrides \
        KeyPair="$KEY_PAIR" \
        DeploymentBucket="$DEPLOYMENT_BUCKET"
}

function delete-stack() {
    aws cloudformation delete-stack --stack-name "$APP_STACK_NAME"
}

function get-ec2-ip() {
    aws cloudformation describe-stacks \
      --stack-name "$APP_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='Ec2Ip'].OutputValue" \
      --output text
}

function get-asg-ec2-public-ip() {
    ASG_NAME=$(aws cloudformation describe-stacks \
      --stack-name "$APP_STACK_NAME" \
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
