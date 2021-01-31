import sys, os
import json
from robot.api import TestSuite
from robot.api import logger
from RFServer.server_interface import RFServerInterface
from dateutil import parser
from distutils.util import strtobool

class RFServerStart(RFServerInterface):
    
    def get_keyword_request(self, json_item: str) -> dict:
        try:
            kw_dict = json.loads(json_item)
            
        except Exception:
            with open(json_item) as json_file:
                kw_dict = json.load(json_file)
        
        kw_dict['expiration'] = parser.parse(kw_dict['expiration'])
        
        if 'exit' in kw_dict:
            kw_dict['exit'] = bool(strtobool(kw_dict['exit'].strip()))
    
        return kw_dict


    def send_keyword_result(self, result: dict) -> dict:
        logger.console(str(result))
        return result


def run():
    try:
        json_path = sys.argv[1]
    except IndexError as e:
        raise IndexError('First and only argument must be path to keyword json!') from e

    suite = TestSuite('RFServer')
    suite.resource.imports.library('RFServer', args = [RFServerStart()])
    test = suite.tests.create('RFserver test')
    test.keywords.create('RFServer.Main Loop', args = [json_path])

    suite.run()


if __name__ == "__main__":
    run()
    



    