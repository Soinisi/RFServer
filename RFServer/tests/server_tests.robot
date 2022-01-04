*** Settings ***
Library             OperatingSystem
Library             ../interfaces/test_interface.py

Test Setup          Setup RFServer          




*** Test Cases ***

Test Keyword Execution Success        
    RFServer.Main Loop  {"sender_id":"test_success", "expiration": "22.1.2999", "keyword":"Log To Console", "kw_args":["Hello world!"], "exit":"true"}
    Should Be Equal As Strings  ${result}   {'sender_id': 'test_success', 'kw_status': 'pass', 'return_value': None}


Test Keyword Execution Fail         
    RFServer.Main Loop  {"sender_id":"test_fail", "expiration": "22.1.2999", "keyword":"Fail", "kw_args":["Expected fail"], "exit":"true"}
    Should Be Equal As Strings  ${result}   {'sender_id': 'test_fail', 'kw_status': 'fail', 'return_value': 'Expected fail'}


Test Keyword Item Expired         
    RFServer.Main Action  {"sender_id":"test_success", "expiration": "1.1.1970", "keyword":"Log To Console", "kw_args":["Hello world!"], "exit":"true"}
    Should Be Equal As Strings  ${result}   {'error': 'item is expired'}


*** Keywords ***

Setup RFServer
    ${interface}=   Get Interface   
    ${conf}=    Evaluate    {'debug': True}
    
    Import Library  RFServer    ${interface}    ${conf} 