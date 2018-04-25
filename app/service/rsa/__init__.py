import base64

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

from ... import config


def rsa_decrypt(encrypted_text):
    with open(config.BASE_DIR + '/app/service/rsa/rsa_private_key.pem', 'r') as f:
        private_rsa_key = f.read()
    rsa_key = RSA.importKey(private_rsa_key)
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    plain_text = cipher.decrypt(base64.b64decode(encrypted_text), 'ERROR')
    return plain_text
