import pytest
from RFServer.data_validator import validate_server_schema, validate_config_schema
from datetime import datetime
from schema import SchemaError, SchemaMissingKeyError

def test_server_data_validation():
    succ_server_data = {'keyword':'test kw', 'sender_id':'test1234', 'expiration': datetime(9999, 1, 1)}
    fail_server_data = {'keyword':'test kw'}

    validate_server_schema(succ_server_data)
    with pytest.raises(SchemaMissingKeyError) as exc_info:
        validate_server_schema(fail_server_data)
       
    assert 'Missing keys:' in str(exc_info)


def test_config_data_validation():
    succ_config = {'server':{'debug': True},'robot': None, 'interface': {'path': 'test_interface'}}
    fail_config = {'server':{'debug':'on'}, 'interface': {'path': 'test_interface'}}
    
    server_conf, robot_conf, interface_conf = validate_config_schema(succ_config)
    
    
    with pytest.raises(SchemaError) as exc_info:
        validate_config_schema(fail_config)
    
    assert "'debug' error" in str(exc_info.value)