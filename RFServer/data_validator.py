from ast import For
from datetime import datetime
from schema import Schema, Optional, Or, Forbidden

SERVER_SCHEMA = Schema({Or('keyword', 'exit'): Or(str, bool),
                        Forbidden('keyword'): bool,
                        Forbidden('exit'): str,
                        Optional('kw_args'): list,
                        Optional('load_lib'): str,
                        Optional('lib_args'): list,
                        'sender_id': str,
                        'expiration': datetime,
                        Optional('interface_data'): dict})


CONFIG_SCHEMA = Schema({'server': Schema({'debug': bool}, ignore_extra_keys = True),
                        'robot': Or(dict, None),
                        'interface': Schema({'path': str}, ignore_extra_keys = True)})



def validate_server_schema(notice_dict):
    SERVER_SCHEMA.validate(notice_dict)
    return notice_dict


def validate_config_schema(config_dict):
    CONFIG_SCHEMA.validate(config_dict)
    return config_dict['server'], config_dict['robot'], config_dict['interface']