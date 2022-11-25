from os import environ
from secrets import token_urlsafe
from hashlib import sha256
from base64 import urlsafe_b64encode


class AuthContext(object):

    def __init__(self):
        self._auth_host = environ['AUTH_HOST']
        print(f"Auth host: {self._auth_host}")
        self._login_path = environ['LOGIN_PATH']
        print(f"Login path: {self._login_path}")
        self._token_path = environ['TOKEN_PATH']
        print(f"Token path: {self._token_path}")
        self._client_id = environ['CLIENT_ID']
        self._client_secret = environ['CLIENT_SECRET']
        self._codeVerifier = token_urlsafe(32)
        print(f"Code verifier: {self._codeVerifier}")
        self._code_challenge = self._hash_code_challenge()
        print(f"Code challenge: {self._code_challenge}")
        self._state = token_urlsafe(32)

    def _hash_code_challenge(self):
        hashed = sha256(self._codeVerifier.encode(encoding='ascii')).digest()
        encoded = urlsafe_b64encode(hashed)
        return encoded.decode('ascii').replace("=", "")

    def get_auth_host(self):
        return self._auth_host

    def get_login_path(self):
        return self._login_path

    def get_token_path(self):
        return self._token_path

    def get_client_id(self):
        return self._client_id

    def get_client_secret(self):
        return self._client_secret

    def get_code_verifier(self):
        return self._codeVerifier

    def get_code_challenge(self):
        return self._code_challenge

    def get_state(self):
        return self._state
