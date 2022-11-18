import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from webbrowser import open
from os import environ
from sys import exit


def parse_auth_code(path):
    return path.split("=")[1]


class Auth:

    # TODO support PKCE flow see https://github.com/googlesamples/oauth-apps-for-windows/blob/master/OAuthConsoleApp/OAuthConsoleApp/Program.cs
    def __init__(self) -> None:
        self._auth_endpoint = environ['AUTH_ENDPOINT']
        print(f"Auth endpoint: {self._auth_endpoint}")
        self._server_ports = map(lambda p: int(p), environ['HTTP_SERVER_PORTS'].split(","))
        http_server = None
        for port in self._server_ports:
            try:
                print(f"Trying to run http server on port: {port}")
                http_server = HTTPServer(('localhost', port), AuthRequestHandler)
                break
            except OSError:
                print(f"port {port} is busy. Trying next one...")
        if http_server is None:
            print(f"Failed to start http server on any of provided ports. Exiting")
            exit(1)
        self._http_server = http_server
        print(f"Server started at {self._http_server.server_address}")
        self._server_port = self._http_server.server_port

    def start_auth_flow(self):
        self._open_auth_request_in_browser()
        self._run_http_server()

    def _open_auth_request_in_browser(self):
        open(f"{self._auth_endpoint}" + f"http://localhost:{self._server_port}")

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
        auth_code = parse_auth_code(self.path)
        print(f"Got auth code: {auth_code}")
        # TODO: do not handle /favicon.ico
        self.send_response(200, "Response OK")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Successful authentication</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><h2>Successful login. You can return to app</h2></body></html>", "utf-8"))
        threading.Thread(target=self.server.shutdown, daemon=True).start()


# run with AUTH_ENDPOINT and HTTP_SERVER_PORTS env variables
if __name__ == '__main__':
    Auth().start_auth_flow()
