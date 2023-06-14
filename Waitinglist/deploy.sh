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

# Install dependencies
pip3 install -r requirements.txt

# Update Lambda function code
if [ -d "venv/lib/python$python_version/site-packages/" ]; then
  cd venv/lib/python"$python_version"/site-packages/ || exit 1
  zip -r ../../../../deploy.zip .
  cd ../../../../ || exit 1
fi
zip -g deploy.zip lambda_function.py response_hanlder.py requirements.txt tests/ .env

# Get the full file path of the deploy.zip file
file_path=$(realpath deploy.zip)

# Update the Lambda function code on AWS
aws lambda update-function-code --function-name DineSeater-$stage-Waitinglist --zip-file "fileb://$file_path"

