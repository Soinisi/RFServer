from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import time
from threading import Thread
from dateutil import parser
from distutils.util import strtobool
from RFServer.server_interface import RFServerInterface

kw_request_global = None
kw_result_global = None

class LocalApiInterface(RFServerInterface):
    def get_keyword_request(self, *args, **kwargs) -> dict:
        global kw_request_global
        req = kw_request_global
        kw_request_global = None
        return req

    def send_keyword_result(self, result: dict, kw_dict: dict) -> dict:
        global kw_result_global
        kw_result_global = result
        return kw_result_global


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
                self.send_response(400, err_message)
                self.end_headers()
                return

            global kw_result_global
            global kw_request_global
            length = int(self.headers.get('content-length'))

            kw_request = json.loads(self.rfile.read(length))
            kw_request = self._parse_kw_request_fields(kw_request)
            kw_request_global = kw_request
        except Exception as err:
            kw_result_global = {'interface_error': str(err)}


        while not kw_result_global:
            time.sleep(0.01)
        res = kw_result_global
        kw_result_global = None

        kw_res_json = json.dumps(res)

        self._set_headers()
        self.wfile.write(kw_res_json.encode())


    def _parse_kw_request_fields(self, kw_request):
        kw_request['expiration'] = parser.parse(kw_request['expiration'])

        if 'exit' in kw_request:
            kw_request['exit'] = bool(strtobool(kw_request['exit'].strip()))
        return kw_request


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


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