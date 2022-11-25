from http.client import HTTPSConnection
from base64 import urlsafe_b64encode

token_uri = "{}?grant_type=authorization_code&client_id={}&code={}&redirect_uri={}&code_verifier={}"


def exchangeCodeForToken(auth_context, redirect_uri, code):
    auth_host = auth_context.get_auth_host()
    client_id = auth_context.get_client_id()
    client_secret = auth_context.get_client_secret()
    auth_header = urlsafe_b64encode(bytes(client_id + ":" + client_secret, 'utf-8')).decode('utf-8')
    connection = HTTPSConnection(auth_host)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + auth_header
    }
    connection.request("POST", _construct_path(auth_context, redirect_uri, code), None, headers)
    response = connection.getresponse()
    print(f"Got response status: {response.status}")
    print(f"Got response body: {response.read()}")


def _construct_path(auth_context, redirect_uri, code):
    token_path = auth_context.get_token_path()
    client_id = auth_context.get_client_id()
    code_verifier = auth_context.get_code_verifier()
    return token_uri.format(token_path, client_id, code, redirect_uri, code_verifier)
