import sys, os
import json
from robot.api import TestSuite
from robot.api import logger
from RFServer.server_interface import RFServerInterface
from dateutil import parser
from distutils.util import strtobool
from importlib import import_module 
from importlib.util import spec_from_file_location, module_from_spec
import re


class RFServerStart(RFServerInterface):
    
    def get_keyword_request(self, json_item: str) -> dict:
        try:
            kw_dict = json.loads(json_item)
            
        except Exception:       
            with open(json_item) as json_file:
                kw_dict = json.load(json_file)

        try:
            kw_dict['expiration'] = parser.parse(kw_dict['expiration'])
            
            if 'exit' in kw_dict:
                kw_dict['exit'] = bool(strtobool(kw_dict['exit'].strip()))
        except Exception:
            return {}
        
        return kw_dict


    def send_keyword_result(self, result: dict, kw_dict) -> dict:
        logger.console(str(result))
        with open('output.json','w+') as output_file:
            json.dump(result, output_file)
        return result


def run_cmd():
    try:
        json_path = sys.argv[2]
    except IndexError as e:
        raise IndexError('Second arg must be json path or json string!') from e
    
    suite = TestSuite('RFServer')
    suite.resource.imports.library('RFServer', args = [RFServerStart()])
    test = suite.tests.create('RFserver test')
    test.keywords.create('RFServer.Main Loop', args = [json_path])

    suite.run(output = 'output.xml')



def run():
    module_path = sys.argv[1]
    if module_path == 'cmd_test':
        run_cmd()
        return
    
    interface_args = sys.argv[2:]
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    interfaces_dir = os.path.join(root_dir, 'interfaces')
    sys.path.append(root_dir)
    sys.path.append(interfaces_dir)

    try:
        interface_mod = import_module(module_path)
    except ModuleNotFoundError:
        module_pattern = re.compile(r'[\\|/]*(.*?)[.]py')
        mod_name = module_pattern.search(module_path).group(1)

        spec = spec_from_file_location(mod_name, module_path)
        interface_mod = module_from_spec(spec)
        spec.loader.exec_module(interface_mod)
    
    if not hasattr(interface_mod, 'get_interface'):
        raise NotImplementedError("'get_interface' function not implemented in loaded module!")
    
    interface = interface_mod.get_interface(*interface_args)

    suite = TestSuite('RFServer', rpa = True)
    suite.resource.imports.library('RFServer', args = [interface])
    test = suite.tests.create('RFserver Task')
    test.keywords.create('RFServer.Main Loop')
    suite.run()


if __name__ == "__main__":
    run()
    



    
