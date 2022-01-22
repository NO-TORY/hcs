import re

from ..hcs import SESSION
from . import crypto
from .keypad import KeyPad
from requests import Session

class mTransKey:
    def __init__(self, servlet_url):
        self.servlet_url = servlet_url
        self.crypto = crypto.Crypto()
        self.token = ""
        self.initTime = ""
        self.decInitTime = ""
        self.qwerty = []
        self.number = []
        self.keyIndex = ""

    def _get_data(self):
        self._get_token(SESSION)
        self._get_init_time(SESSION)
        self._get_public_key(SESSION)
        self._get_key_info(SESSION)

    def _get_token(self, session: Session):
        with session.get("{}?op=getToken".format(self.servlet_url)) as resp:
            txt = resp.text
            self.token = re.findall("var TK_requestToken=(.*);", txt)[0]

    def _get_init_time(self, session: Session):
        with session.get("{}?op=getInitTime".format(self.servlet_url)) as resp:
            txt = resp.text
            self.initTime = re.findall("var initTime='(.*)';", txt)[0]

    def _get_public_key(self, session: Session):
        with session.post(self.servlet_url, data={
                "op": "getPublicKey",
                "TK_requestToken": self.token
            }
        ) as resp:
            key = resp.text
            self.crypto.set_pub_key(key)

    def _get_key_info(self, session: Session):
        with session.post(
            self.servlet_url,
            data={
                "op": "getKeyInfo",
                "key": self.crypto.get_encrypted_key(),
                "transkeyUuid": self.crypto.uuid,
                "useCert": "true",
                "TK_requestToken": self.token,
                "mode": "common",
            },
        ) as resp:
            key_data = resp.text
            qwerty, num = key_data.split("var number = new Array();")

            qwerty_keys = []
            number_keys = []

            for p in qwerty.split("qwertyMobile.push(key);")[:-1]:
                points = re.findall("key\.addPoint\((\d+), (\d+)\);", p)
                qwerty_keys.append(points[0])

            for p in num.split("number.push(key);")[:-1]:
                points = re.findall("key\.addPoint\((\d+), (\d+)\);", p)
                number_keys.append(points[0])

            self.qwerty = qwerty_keys
            self.number = number_keys

    def new_keypad(self, key_type, name, inputName, fieldType="password"):
        self._get_data()
        with SESSION as session:
            key_index_res = session.post(
                self.servlet_url,
                data={
                    "op": "getKeyIndex",
                    "name": "password",
                    "keyType": "single",
                    "keyboardType": "number",
                    "fieldType": "password",
                    "inputName": "password",
                    "parentKeyboard": "false",
                    "transkeyUuid": self.crypto.uuid,
                    "exE2E": "false",
                    "TK_requestToken": self.token,
                    "isCrt": "false",
                    "allocationIndex": "3011907012",
                    "keyIndex": "",
                    "initTime": self.initTime,
                    "talkBack": "true"
                }
            )
            self.keyIndex = key_index_res.text

            with session.post(
                self.servlet_url,
                data={
                    "op": "getDummy",
                    "name": name,
                    "keyType": "single",
                    "keyboardType": "number",
                    "fieldType": fieldType,
                    "inputName": inputName,
                    "transkeyUuid": self.crypto.uuid,
                    "exE2E": "false",
                    "isCrt": "false",
                    "allocationIndex": "3011907012",
                    "keyIndex": self.keyIndex,
                    "initTime": self.initTime,
                    "TK_requestToken": self.token,
                    "dummy": "undefined",
                    "talkBack": "true",
                },
            ) as resp:
                skip_data = resp.text
                skip = skip_data.split(",")

                return KeyPad(self.crypto, key_type, skip, self.number, self.initTime)

    def hmac_digest(self, message):
        return self.crypto.hmac_digest(message)

    def get_uuid(self):
        return self.crypto.uuid