from http.server import BaseHTTPRequestHandler
import json
import cgi
from RFServer.server_interface import RFServerInterface

class LocalHttpServerInterface(RFServerInterface, BaseHTTPRequestHandler):

    def __init__(self):
        self.kw_message = None
        self.kw_result = None


    def get_keyword_request(self, *args, **kwargs) -> dict:
        return super().get_keyword_request(*args, **kwargs)


    def send_keyword_result(self, result: dict, kw_dict: dict) -> dict:
        return super().send_keyword_result(result, kw_dict)


    def do_POST(self):
        ctype, _ = cgi.parse_header(self.headers.get('content-type'))
        if ctype != 'application/json':
            self.send_response(400, 'content type not json')
            self.end_headers()
            return
        length = int(self.headers.get('content-length'))
        self.kw_message = json.loads(self.rfile.read(length))
        while