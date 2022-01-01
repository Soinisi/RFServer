from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from RFServer.data_validator import validate_schema
import time
from datetime import datetime, timedelta
from RFServer.server_interface import RFServerInterface



run_kw = BuiltIn().run_keyword
import_lib = BuiltIn().import_library


class RFServer:
    def __init__(self, interface):
        if not issubclass(type(interface), RFServerInterface):
            raise TypeError('interface does not have RFServerInterface as parent class!')
        
        self.interface = interface


    def main_loop(self, *args, **kwargs):
        run_server = True
        while run_server:
            run_server = self.main_action(*args, **kwargs)
            time.sleep(0.1)


    def main_action(self, *args, **kwargs):
        
        kw_dict = self._get_keyword_request(*args, **kwargs)
        
        if kw_dict:
            try:
                kw_dict = validate_schema(kw_dict)
            except Exception as e:
                self._send_keyword_result({'error': str(e)}, kw_dict)   
                return True

            if not self._expired_item(kw_dict):
                self._import_library(kw_dict)
                self._run_kw_with_error_handler(kw_dict)
            
                if 'exit' in kw_dict and kw_dict['exit'] is True:
                    logger.info('Exiting RFServer', also_console = True)
                    return False

            else:
                logger.warn('item with sender_id "' + kw_dict['sender_id'] + '" is expired!')
                self._send_keyword_result({'error': 'item is expired'}, kw_dict)

            

        return True




#HELPERS------------------------------------------------------------------------------    
    def _get_keyword_request(self, *args, **kwargs):
        try:
            return self.interface.get_keyword_request(*args, **kwargs)
        except Exception as e:
            logger.error('get keyword request error: ' + str(e))
            return {}


    def _send_keyword_result(self, result, kw_dict):
        try:
            return self.interface.send_keyword_result(result, kw_dict)
        except Exception as e:
            logger.error('send keyword request error: ' + str(e))
            return {}


    def _import_library(self, kw_dict: dict):
        if 'load_lib' in kw_dict and kw_dict['load_lib']:
            args = kw_dict['lib_args'] if 'lib_args' in kw_dict else []
            try:
                import_lib(kw_dict['load_lib'], *args)
                logger.info(kw_dict['load_lib'] + ' loaded', also_console = True)
            except Exception as e:
                logger.error(str(e))
    

    def _run_kw_with_error_handler(self, kw_dict: dict):
        
        if 'keyword' in kw_dict and kw_dict['keyword']:
            result_dict = {'sender_id': kw_dict['sender_id'],
                           'kw_status': '', 
                           'return_value': None}

            try:
                args = kw_dict['kw_args'] if 'kw_args' in kw_dict else []
                val = run_kw(kw_dict['keyword'], *args)
                result_dict['kw_status'] = 'pass'
                result_dict['return_value'] = val
                
            except Exception as e:
                result_dict['kw_status'] = 'fail'
                result_dict['return_value'] = str(e)
                
            response = self._send_keyword_result(result_dict, kw_dict)
            logger.info(str(response))

        
    def _expired_item(self, kw_dict):
        return datetime.now() > kw_dict['expiration']

