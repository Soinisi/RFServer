import sys
import json
from robot.api import TestSuite
from robot.api import logger
from RFServer.server_interface import RFServerInterface
from dateutil import parser


class RFServerStart(RFServerInterface):
    
    def get_keyword_request(self, json_path: str) -> dict:
        
        with open(json_path) as json_file:
            kw_dict = json.load(json_file)
        
        kw_dict['expiration'] = parser.parse(kw_dict['expiration'])
        
        if 'exit' in kw_dict:
            kw_dict['exit'] = eval(kw_dict['exit'].strip().capitalize())
    
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
    



    