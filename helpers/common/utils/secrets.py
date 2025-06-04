from __future__ import annotations

import json
import boto3
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secrets(**kwargs) -> dict:
    secret_name = kwargs.get("secret_name", "")
    client = boto3.client('secretsmanager')
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_value = response['SecretString']
        return json.loads(secret_value)
    except Exception as e:
        logger.info(f"Failed to get secret {secret_name}: {e}")
        return {}


def put_secret(**kwargs) -> dict:
    secret_name = kwargs.get("secret_name", "")
    secret_value = kwargs.get("secret_value", "")
    description = kwargs.get("description", "default description")
    client = boto3.client('secretsmanager')
    
    try:
        response = client.create_secret(Name=secret_name, SecretString=json.dumps(secret_value), Description=description)
        return response
    except Exception as e:
        logger.info(f"Failed to put secret {secret_name}: {e}")
        return {}
