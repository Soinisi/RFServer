import pytest
from libraries.data_validator import validate_schema


def test_data_validation():
    test_single = {'keywords': [{'keyword:' 'test'}]}
    test_data = {'keywords': [{'keyword:' 'test'}]}