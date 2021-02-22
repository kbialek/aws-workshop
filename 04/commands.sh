#!/usr/bin/env bash
set -euf -o pipefail +o allexport

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
    rm demo-app.zip
    cd demo-app
    zip -r ../demo-app.zip . -x \*__pycache__*
    cd -
}

function app-upload() {
  BUCKET=$(get-deployment-bucket)
  aws s3 cp demo-app.zip "s3://$BUCKET/"
}

### Application Stack

function deploy-stack() {
    APP_STACK_NAME="AppStack-$2"
    template_file="template-$2.yaml"
    DEPLOYMENT_BUCKET=$(get-deployment-bucket)
    aws cloudformation deploy \
      --stack-name "$APP_STACK_NAME" \
      --template-file "$template_file" \
      --capabilities CAPABILITY_IAM \
      --parameter-overrides \
        KeyPair="$KEY_PAIR" \
        DeploymentBucket="$DEPLOYMENT_BUCKET" \
        DbiResourceId="db-7VXXNFNYTY4U42DLLK7W7W4LKA"
}

function delete-stack() {
    APP_STACK_NAME="AppStack-$2"
    aws cloudformation delete-stack --stack-name "$APP_STACK_NAME"
}

function get-ec2-ip() {
    APP_STACK_NAME="AppStack-$2"
    aws cloudformation describe-stacks \
      --stack-name "$APP_STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='Ec2Ip'].OutputValue" \
      --output text
}

$1 "$@"
