from RFServer.server_interface import RFServerInterface
import json
from dateutil import parser
from distutils.util import strtobool
from robot.libraries.BuiltIn import BuiltIn



class TestInterface(RFServerInterface):
    
        
    
    def get_keyword_request(self, *args, **kwargs) -> dict:
        kw_dict = json.loads(args[0])
        kw_dict['expiration'] = parser.parse(kw_dict['expiration'])
            
        if 'exit' in kw_dict:
            kw_dict['exit'] = bool(strtobool(kw_dict['exit'].strip()))
        
        return kw_dict


    def send_keyword_result(self, result: dict, kw_dict: dict) -> dict:
        BuiltIn().run_keyword('Set Test Variable', '${result}', str(result))
        return {}



def get_interface(*args, **kwargs):
    return TestInterface()