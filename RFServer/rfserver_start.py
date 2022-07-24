import sys, os
from robot.api import TestSuite
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
import re
from yaml import safe_load
from robot.version import VERSION
from packaging import version
from RFServer.data_validator import validate_config_schema


def run():
    config_path = sys.argv[1]

    root_dir = os.path.dirname(os.path.abspath(__file__))
    interfaces_dir = os.path.join(root_dir, 'interfaces')
    sys.path.append(root_dir)
    sys.path.append(interfaces_dir)

    with open(config_path, 'r') as yaml_file:
        config_dict = safe_load(yaml_file)

    server_conf, robot_conf, interface_conf = validate_config_schema(config_dict)

    interface_args = sys.argv[2:]

    module_path = interface_conf.pop('path')
    interface_mod = _load_module(module_path)

    if not hasattr(interface_mod, 'get_interface'):
        raise NotImplementedError("'get_interface' function not implemented in loaded module!")

    interface = interface_mod.get_interface(*interface_args, **interface_conf)

    _start_server(interface, server_conf, robot_conf)


#Helpers-------------------------------------------------------------------------

def _load_module(module_path):
    try:
        interface_mod = import_module(module_path)
    except ModuleNotFoundError:
        module_pattern = re.compile(r'[\\|/]*(.*?)[.]py')
        mod_name = module_pattern.search(module_path).group(1)
        spec = spec_from_file_location(mod_name, module_path)
        interface_mod = module_from_spec(spec)
        spec.loader.exec_module(interface_mod)

    return interface_mod


def _start_server(interface, server_conf, robot_conf):
    suite = TestSuite('RFServer', rpa = True)
    suite.resource.imports.library('RFServer', args = [interface, server_conf])
    test = suite.tests.create('RFserver Task')

    if version.parse(VERSION) < version.parse('4.0.0'):
        test.keywords.create('RFServer.Main Loop')
    else:
        test.body.create_keyword('RFServer.Main Loop')
    suite.run(**robot_conf)




if __name__ == "__main__":
    run()





