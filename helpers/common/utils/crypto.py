from __future__ import annotations

import os
import base64
import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def load_private_key(**kwargs):
    file_path = kwargs.get("file_path", "/opt/keys")
    file_name = kwargs.get("file_name", "")
    file_key_path = os.path.join(file_path, file_name)

    try:
        with open(file_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        return private_key
    
    except Exception as error:
        logger.error(f"Failed to load private key={file_name}. Error: {error}")
        return None
    
    
def load_public_key(**kwargs):
    file_path = kwargs.get("file_path", "/opt/configurations/keys")
    file_name = kwargs.get("file_name", "")
    file_key_path = os.path.join(file_path, file_name)

    try:
        with open(file_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        return public_key
    except Exception as error:
        logger.error(f"Failed to load public key={file_name}. Error: {error}")
        return None


def rsa_encrypt(**kwargs):
    original_value = kwargs.get("original_value", "")
    public_key = kwargs.get("public_key", None)

    try:
        encrypted_value = public_key.encrypt(
            original_value,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_value
    
    except Exception as error:
        logger.error(f"Failed to rsa encrypt={original_value}. Error: {error}")
        return None


def rsa_decrypt(**kwargs):
    private_key = kwargs.get("private_key", None)
    encrypted_value = kwargs.get("encrypted_value", "")
    encrypted_value_type = kwargs.get("encrypted_value_type", "base64")

    try:
        if encrypted_value_type == "base64":
            encrypted_value = base64.b64decode(encrypted_value.encode("utf-8"))
    
        decrypted_value = private_key.decrypt(
            encrypted_value,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_value
    
    except Exception as error:
        logger.error(f"Failed to rsa decrypt decrypt={encrypted_value}. Error: {error}")
        return None



