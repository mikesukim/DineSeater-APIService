# Waitinglist API

## Background
The Waitinglist API can only be accessed through AWS Lambda via API Gateway. It supports HTTP requests for both GET and POST methods.

## Requirement
- python version 3.10
- [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## Before Deployment
1. activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
2. install dependencies
```bash
pip install -r dev-requirements.txt
# requirements.txt is only for production. 
# requirements.txt will include packages thar are only needed in Lambda environment, 
# and exclude packages that are required for only development (e.x. boto3 & pytest). 
```
3. run pytest and make sure all tests pass.
```bash
pytest tests
```

4. **make sure on requirements.txt, has only the packages that are not needed in Lambda environment.** For example, Boto3 is already available in Lambda environment, so it should not be listed in requirements.txt. Pytest is only needed for development, so it should not be listed in requirements.txt either.

## Deployment
1. Make sure aws-cli configured correctly. Creating access & secret keys for aws-cli at AWS IAM console might require, if was not created previously.
```bash
aws configure
```

2. execute deploy.sh
```bash
sh deploy.sh <your_python_version>  <stage:case_sensitive>
# e.g. sh deploy.sh 3.10 dev
```