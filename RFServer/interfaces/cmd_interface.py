import json
from robot.api import logger
from dateutil import parser
from distutils.util import strtobool
from RFServer.server_interface import RFServerInterface

class RFServerStart(RFServerInterface):
    
    def __init__(self, json_item):
        self.json_item =json_item

    def get_keyword_request(self) -> dict:
        try:
            kw_dict = json.loads(self.json_item)
            
        except Exception:       
            with open(self.json_item) as json_file:
                kw_dict = json.load(json_file)

        try:
            kw_dict['expiration'] = parser.parse(kw_dict['expiration'])
            
            if 'exit' in kw_dict:
                kw_dict['exit'] = bool(strtobool(kw_dict['exit'].strip()))
        except Exception:
            return {}
        
        return kw_dict


    def send_keyword_result(self, result: dict, kw_dict) -> dict:
        return result



def get_interface(*args, **kwargs):
    return RFServerStart(*args)