#!/bin/bash

python_version=$1
stage=$2

if [ -z "$python_version" ]; then
  echo "Please provide the Python version as an argument."
  exit 1
fi

if [ -z "$stage" ]; then
  echo "Please provide the deployment stage as an argument. e.g. Test or Prod (case sensitive)"
  exit 1
fi

# Activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Check if dist folder exists, if so, delete it and create new one
if [ -d "dist" ]; then
  rm -rf dist
fi
mkdir -p dist

# Install dependencies
pip3 install --target ./dist -r requirements.txt

# Zip sources
cd dist
zip -r ../dist.zip .
cd ..
zip -r dist.zip source
zip -g dist.zip lambda_function.py .env

# Get the full file path of the dist.zip file
file_path=$(realpath dist.zip)

# Update the Lambda function code on AWS
aws lambda update-function-code --function-name DineSeater-$stage-DeviceTokenRegistration --zip-file "fileb://$file_path"

# once the deployment is done, delete the dist folder and the dist.zip file
rm dist.zip