import threading
from base64 import urlsafe_b64encode
from hashlib import sha256
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import environ
from secrets import token_urlsafe
from sys import exit
from webbrowser import open
from util import search_code_path


class Auth:

    def __init__(self) -> None:
        self._auth_endpoint = environ['AUTH_ENDPOINT']
        print(f"Auth endpoint: {self._auth_endpoint}")
        self._client_id = environ['CLIENT_ID']
        self._server_ports = map(lambda p: int(p), environ['HTTP_SERVER_PORTS'].split(","))
        print(f"Http server ports: {self._server_ports}")
        self._http_server = self._setupHttpServer()
        self._server_port = self._http_server.server_port
        self._state = token_urlsafe(32)
        self._codeVerifier = token_urlsafe(32)
        self._code_challenge = self._hash_code_challenge()

    def _setupHttpServer(self):
        for port in self._server_ports:
            try:
                print(f"Trying to run http server on port: {port}")
                http_server = HTTPServer(('localhost', port), AuthRequestHandler)
                print(f"Server started at {http_server.server_address}")
                return http_server
            except OSError:
                print(f"port {port} is busy. Trying next one...")
        print(f"Failed to start http server on any of provided ports. Exiting...")
        exit(1)

    def _hash_code_challenge(self):
        hashed = sha256(self._codeVerifier.encode(encoding='ascii')).digest()
        encoded = urlsafe_b64encode(hashed)
        return encoded.decode('ascii')

    def start_auth_flow(self):
        self._open_auth_request_in_browser()
        self._run_http_server()

    def _open_auth_request_in_browser(self):
        redirect_uri = f"http://localhost:{self._server_port}"
        login_url = "{}?response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile" \
                    "&redirect_uri={}&client_id={}&state={}&code_challenge={}&code_challenge_method=S256"\
            .format(self._auth_endpoint, redirect_uri, self._client_id, self._state, self._code_challenge)
        open(login_url)

    def _run_http_server(self):
        try:
            self._http_server.serve_forever()
        except KeyboardInterrupt:
            print("Program interrupted by user")
            pass
        finally:
            print("Closing server...")
            self._http_server.server_close()


class AuthRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        code = search_code_path(path, "code")
        state = search_code_path(path, "state")
        print(f"Got code: {code}")
        print(f"Got state: {state}")
        # TODO: do not handle /favicon.ico
        self.send_response(200, "Response OK")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Successful authentication</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><h2>Successful login. You can return to app</h2></body></html>", "utf-8"))
        threading.Thread(target=self.server.shutdown, daemon=True).start()


if __name__ == '__main__':
    Auth().start_auth_flow()
