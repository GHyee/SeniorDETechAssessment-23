#!/bin/bash

set -e

case "$1" in
  webserver)
    echo "Setting AWS credentials..."
    export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
    export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
    export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

    echo "Downloading files from S3..."
    aws s3 cp s3://${S3_BUCKET_NAME}/cloud_data_pipeline/ cloud_data_pipeline/ --recursive
    echo "Initializing airflow..."
    docker-compose up --build

    echo "Setting AWS credentials..."
    export AWS_ACCESS_KEY_ID=$AWS

    # Install s3fs-fuse
    apt-get update && \
    apt-get install -y s3fs

    # Mount S3 bucket to a directory
    echo "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" > ~/.passwd-s3fs && \
    chmod 600 ~/.passwd-s3fs && \
    mkdir /mnt/s3 && \
    s3fs $S3_BUCKET_NAME /mnt/s3 -o passwd_file=~/.passwd-s3fs -o umask=0022 -o uid=1000 -o gid=1000

