import pytest
from RFServer.data_validator import validate_server_schema, validate_config_schema
from datetime import datetime
from schema import SchemaError, SchemaMissingKeyError

def test_server_data_validation_success():
    succ_no_exit_data = {'keyword':'test kw', 'sender_id':'test1234', 'expiration': datetime(9999, 1, 1)}
    succ_no_keyword_data = {'exit': True, 'sender_id':'test1234', 'expiration': datetime(9999, 1, 1)}

    assert validate_server_schema(succ_no_exit_data)
    assert validate_server_schema(succ_no_keyword_data)


def test_server_data_validation_fail():
    fail_mandatory_data = {'keyword':'test kw'}
    fail_no_actions_data = {'sender_id':'test1234', 'expiration': datetime(9999, 1, 1)}

    with pytest.raises(SchemaMissingKeyError) as exc_info:
        validate_server_schema(fail_mandatory_data)
    assert 'Missing keys:' in str(exc_info)

    with pytest.raises(SchemaMissingKeyError) as exc_info:
        validate_server_schema(fail_no_actions_data)
    assert 'Missing key:' in str(exc_info)


def test_config_data_validation():
    succ_config = {'server':{'debug': True},'robot': None, 'interface': {'path': 'test_interface'}}
    fail_config = {'server':{'debug':'on'}, 'interface': {'path': 'test_interface'}}

    server_conf, robot_conf, interface_conf = validate_config_schema(succ_config)


    with pytest.raises(SchemaError) as exc_info:
        validate_config_schema(fail_config)

    assert "'debug' error" in str(exc_info.value)