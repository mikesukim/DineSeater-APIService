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
# make sure you are at Waitinglist directory
# Make sure python version is 3.10 above. Also make sure your pip version is matched with your python version. 
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m unittest discover
```

2. Make sure aws-cli configured correcrly. Creating access & secret keys for aws-cli at AWS IAM console might require, if was not created previously.
```bash
aws configure
```

3. execute deploy.sh
```bash
sh deploy.sh <your_python_version> <stage:case_sensitive>
# e.g. sh deploy.sh 3.10 Test
```