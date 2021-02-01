#!/usr/bin/env bash
set -euf -o pipefail +o allexport

STACK_NAME="MyEc2Stack"
KEY_PAIR="kbialek"

function deploy-stack() {
    template_file="template-$2.yaml"
    aws cloudformation deploy \
      --stack-name "$STACK_NAME" \
      --template-file "$template_file" \
      --capabilities CAPABILITY_IAM \
      --parameter-overrides \
        KeyPair="$KEY_PAIR"
}

function delete-stack() {
    aws cloudformation delete-stack --stack-name "$STACK_NAME"
}

function get-ec2-ip() {
    aws cloudformation describe-stacks \
      --stack-name "$STACK_NAME" \
      --query "Stacks[0].Outputs[?OutputKey=='Ec2Ip'].OutputValue" \
      --output text
}

$1 "$@"
