import os
from threading import Thread
from pathlib import Path
import requests
from requests.exceptions import ConnectionError
import pytest

LOCAL_HTTP_SERVER_ADDRESS = 'http://localhost:8000/keyword'

def test_run_keyword_get_return():
    server_path = str(Path(__file__).parent / 'res' / 'http_test_conf.yaml')
    server_cmd = 'rf_server ' + server_path
    server_thread = Thread(target = os.system, args = (server_cmd,))
    server_thread.start()
    server_thread.join(5)

    kw_req_dict = {"expiration":"18.09.2099",
                "sender_id":"123",
                "keyword":"convert to string",
                "kw_args":[100],
                "exit":"True"}

    res = requests.post(LOCAL_HTTP_SERVER_ADDRESS, json = kw_req_dict)
    kw_answ_dict = res.json()
    assert kw_answ_dict['sender_id'] == '123'
    assert kw_answ_dict['kw_status'] == 'pass'
    assert kw_answ_dict['return_value'] == '100'

def test_run_keyword_get_error():
    server_path = str(Path(__file__).parent / 'res' / 'http_test_conf.yaml')
    server_cmd = 'rf_server ' + server_path
    server_thread = Thread(target = os.system, args = (server_cmd,))
    server_thread.start()
    server_thread.join(5)

    kw_req_dict = {"expiration":"18.09.2099",
                "sender_id":"234",
                "keyword":"random keyword",
                "kw_args":[100],
                "exit":"True"}

    res = requests.post(LOCAL_HTTP_SERVER_ADDRESS, json = kw_req_dict)
    kw_answ_dict = res.json()

    assert kw_answ_dict['sender_id'] == '234'
    assert kw_answ_dict['kw_status'] == 'fail'
    assert kw_answ_dict['return_value'] == "No keyword with name 'random keyword' found."

def test_run_exit():
    server_path = str(Path(__file__).parent / 'res' / 'http_test_conf.yaml')
    server_cmd = 'rf_server ' + server_path

    server_thread = Thread(target = os.system, args = (server_cmd,))
    server_thread.start()
    server_thread.join(5)

    kw_req_dict = {"expiration":"18.09.2099",
                "sender_id":"345",
                "exit":"True"}

    res = requests.post(LOCAL_HTTP_SERVER_ADDRESS, json = kw_req_dict)
    kw_answ_dict = res.json()
    assert kw_answ_dict['sender_id'] == '345'
    with pytest.raises(ConnectionError) as exc_info:
        requests.post(LOCAL_HTTP_SERVER_ADDRESS, json = kw_req_dict)

    assert 'Connection aborted.' in str(exc_info)
