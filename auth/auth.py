import threading
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import environ
from sys import exit
from webbrowser import open

from kivy.clock import Clock

from auth.auth_context import AuthContext
from auth.auth_token_exchange import exchangeCodeForToken
from auth.util import search_code_path, format_redirect_uri


def authenticate_user(callback=None):
    auth_context = AuthContext()
    server_ports = map(lambda p: int(p), environ['HTTP_SERVER_PORTS'].split(","))
    auth_server = create_http_server(server_ports, auth_context, callback)
    open_auth_request_in_browser(auth_server.server_port, auth_context)
    run_http_server(auth_server)


class AuthRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, auth_flow_context, callback, *args, **kwargs):
        self._auth_context = auth_flow_context
        self._callback = callback
        super().__init__(*args, **kwargs)

    def do_GET(self):
        path = self.path
        incoming_code = search_code_path(path, "code")
        incoming_state = search_code_path(path, "state")
        print(f"Got code: {incoming_code}")
        print(f"Got state: {incoming_state}")
        # TODO: do not handle /favicon.ico
        if self._auth_context.get_state() != incoming_state:
            print(f"Received request with invalid PKCE state")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Authorization failed</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><h2>Authorization failed</h2></body></html>", "utf-8"))
        else:
            self.send_response(200, "Response OK")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Successful authentication</title></head>", "utf-8"))
            self.wfile.write(bytes("<body><h2>Successful login. You can return to app</h2></body></html>", "utf-8"))
            exchangeCodeForToken(self._auth_context, format_redirect_uri(self.server.server_address[1]), incoming_code)
        Clock.schedule_once(self._callback, -1)
        threading.Thread(target=self.server.shutdown, daemon=True).start()


def open_auth_request_in_browser(server_port, auth_flow_context):
    auth_host = auth_flow_context.get_auth_host()
    login_path = auth_flow_context.get_login_path()
    redirect_uri = format_redirect_uri(server_port)
    client_id = auth_flow_context.get_client_id()
    state = auth_flow_context.get_state()
    code_challenge = auth_flow_context.get_code_challenge()
    login_url = "https://{}{}?response_type=code&scope=aws.cognito.signin.user.admin+email+openid+phone+profile" \
                "&redirect_uri={}&client_id={}&state={}&code_challenge={}&code_challenge_method=S256" \
        .format(auth_host, login_path, redirect_uri, client_id, state, code_challenge)
    open(login_url)


def create_http_server(ports, auth_flow_context, callback):
    for port in ports:
        try:
            print(f"Trying to run http server on port: {port}")
            server = HTTPServer(('localhost', port), partial(AuthRequestHandler, auth_flow_context, callback))
            print(f"Server started at {server.server_address}")
            return server
        # TODO: handle other possible OSError failures
        except OSError:
            print(f"port {port} is busy. Trying next one...")
    print(f"Failed to start http server on any of provided ports. Exiting...")
    exit(1)


def run_http_server(server):
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Program interrupted by user")
        pass
    finally:
        print("Closing server...")
        server.server_close()


if __name__ == '__main__':
    authenticate_user()
