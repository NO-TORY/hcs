# -*- coding: utf-8 -*-

import hashlib
import hmac
import os
from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA

from . import seed

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import Self

pubkey = (
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2"
    "+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr"
    "+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K5xJEppHG0qc"
    "+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv8BM"
    "/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB== "
)

def encrypt(n):
    rsa_public_key = b64decode(pubkey)
    pub_key = RSA.importKey(rsa_public_key)
    cipher = PKCS1_v1_5.new(pub_key)
    msg = n.encode("utf-8")
    length = 245

    msg_list = [msg[i : i + length] for i in list(range(0, len(msg), length))]

    encrypt_msg_list = [
        b64encode(cipher.encrypt(message=msg_str)) for msg_str in msg_list
    ]

    return encrypt_msg_list[0].decode("utf-8")
    
class Crypto:
    def __init__(self):
        self.uuid = os.urandom(int(32)).hex()
        self.genSessionKey = os.urandom(int(8)).hex()
        self.key = None
        self.sessionKey = [int(i, 16) for i in list(self.genSessionKey)]

    def _pad(self, txt):
        if len(txt) < 16:
            txt += b"\x00" * (16 - len(txt))
        return txt

    def rsa_encrypt(self, data):
        cipher = PKCS1_OAEP.new(key=self.key, hashAlgo=SHA1)
        return cipher.encrypt(data).hex()

    def get_encrypted_key(self):
        return self.rsa_encrypt(self.genSessionKey.encode())

    def hmac_digest(self, msg):
        # type: ("Self", bytes) -> str
        return hmac.new(
            msg=msg, key=self.genSessionKey.encode(), digestmod=hashlib.sha256
        ).hexdigest()

    def seed_encrypt(self, iv, data):
        s = seed.SEED()
        round_key = s.SeedRoundKey(bytes(self.sessionKey))
        return s.my_cbc_encrypt(self._pad(data), round_key, iv)

    def set_pub_key(self, b64):
        data = b64decode(b64)
        self.key = RSA.import_key(data)
