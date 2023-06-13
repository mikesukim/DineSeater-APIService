# Waitinglist API

## Background
The DeviceToken Registration API can only be accessed through AWS Lambda via API Gateway. It supports only HTTP POST method.

## Requirement
- python version 3.10
## Requirement for deployment
- [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## Deployment
1. Run unit testing and make sure all are passing.
```bash
python -m unittest discover
```

2. Make sure aws-cli configured correcrly. Creating access & secret keys for aws-cli at AWS IAM console might require, if was not created previously.
```bash
aws configure
```

3. Zip all files.
```bash
# copy source code to /source_code
sudo mkdir source_code
cp -r lambda_function.py source_code/
cp -r response_handler.py source_code/
cp -r dineseater-gilsonapp-firebase-adminsdk-credentials.json source_code/
cp -r .env source_code/
cp -r .requirements.txt source_code/

# install dependencies to /source_code
pip install -r requirements.txt -t source_code/

# zip /source_code and save to upper directory
cd source_code
zip -r ../source_code.zip .
```

4. Deploy the zip file
```bash
aws lambda update-function-code --function-name DineSeater-Test-DeviceTokenRegistration --zip-file fileb:///Users/michaelkim/Development/DineSeater/DineSeater-APIService/DeviceTokenRegistration/source_code.zip
```