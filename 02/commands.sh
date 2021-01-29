#!/usr/bin/env bash
set -euf -o pipefail +o allexport

STACK_NAME="MyEc2Stack"

function deploy-stack() {
    template_file="template-$2.yaml"
    aws cloudformation deploy \
      --stack-name "$STACK_NAME" \
      --template-file "$template_file" \
      --capabilities CAPABILITY_IAM
}

function delete-stack() {
    aws cloudformation delete-stack --stack-name "$STACK_NAME"
}

$1 "$@"
