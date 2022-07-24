from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import time
from threading import Thread
import sys
from dateutil import parser
from distutils.util import strtobool
from RFServer.server_interface import RFServerInterface

kw_request = None
kw_result = None

class LocalApiInterface(RFServerInterface):
    def get_keyword_request(self, *args, **kwargs) -> dict:
        global kw_request
        req = kw_request
        kw_request = None
        return req

    def send_keyword_result(self, result: dict, kw_dict: dict) -> dict:
        global kw_result
        kw_result = result
        return kw_result


class LocalHttpServer(BaseHTTPRequestHandler):


    def do_POST(self):
        try:
            ctype, _ = cgi.parse_header(self.headers.get('content-type'))

            err_message = None
            if self.path.lower() != '/keyword':
                err_message = 'address url invalid'
            elif ctype != 'application/json':
                err_message = 'content type not json'

            if err_message:
                self.send_response(400, 'content type not json')
                self.end_headers()
                return

            global kw_result
            global kw_request
            length = int(self.headers.get('content-length'))

            kw_request = json.loads(self.rfile.read(length))
            kw_request['expiration'] = parser.parse(kw_request['expiration'])

            if 'exit' in kw_request:
                kw_request['exit'] = bool(strtobool(kw_request['exit'].strip()))
        except Exception as err:
            kw_result = {'interface_error': str(err)}


        while not kw_result:
            time.sleep(0.05)
        res = kw_result
        kw_result = None

        kw_res_json = json.dumps(res)

        self._set_headers()
        self.wfile.write(kw_res_json.encode())


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


def run_server(http_server, port):
    print('starting httpd in port')


def get_interface(**kwargs):
    port = kwargs.get('port', 8000)
    server_address = ('', port)

    http_server = HTTPServer(server_address, LocalHttpServer)
    server_thread = Thread(target=http_server.serve_forever, daemon=True)
    server_thread.start()

    server_interface = LocalApiInterface()
    return server_interface

if __name__=='__main__':
    get_interface()