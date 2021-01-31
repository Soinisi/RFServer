from datetime import datetime
from schema import Schema, Optional

SERVER_SCHEMA = Schema({Optional('keyword'): str,
                        Optional('kw_args'): list,
                        Optional('load_lib'): str,
                        Optional('lib_args'): list,
                        'sender_id': str,
                        'expiration': datetime,
                        Optional('exit'): bool })

#is this sound at some point?
#KEYWORDS_DICT_SCHEMA = Schema({'keyword': str,
#                        Optional('args'): list})



def validate_schema(notice_dict):
    
    SERVER_SCHEMA.validate(notice_dict)

    #is this sound at some point?
    #if 'keywords' in notice_dict:
    #    for kw_dict in notice_dict['keywords']:
    #        KEYWORDS_DICT_SCHEMA.validate(kw_dict)

    return notice_dict