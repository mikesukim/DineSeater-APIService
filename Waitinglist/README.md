# Waitinglist API

## Background
The Waitinglist API can only be accessed through AWS Lambda via API Gateway. It supports HTTP requests for both GET and POST methods.

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
zip -r lambda_function.zip lambda_function.py tests
```

4. Deploy the zip file
```bash
aws lambda update-function-code \
    --function-name DineSeater-<stage>-Waitinglist \
    --zip-file fileb://<path_to_zip_file>
```