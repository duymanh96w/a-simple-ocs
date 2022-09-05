from fastapi import BackgroundTasks

from app.crud import mobile
from app import redis_op

import json
from bson.objectid import ObjectId


def test_read_billing_info_no_cache(test_app, monkeypatch):
    test_resp_payload = {
        "username": "user_test",
        "call_count": 10,
        "call_block": 30
    }

    async def mock_get_billing_info(username, db):
        return test_resp_payload

    
    def mock_get(key, rdb):
        return None

    
    def mock_setex(key, ttl, value, rdb):
        return None

    monkeypatch.setattr(redis_op, "get", mock_get)
    monkeypatch.setattr(redis_op, "setex", mock_setex)
    monkeypatch.setattr(mobile, "get_billing_info", mock_get_billing_info)
    

    response = test_app.get('/api/v1/mobile/user_test/billing')

    assert response.status_code == 200
    assert response.json() == test_resp_payload


def test_read_billing_info_cache(test_app, monkeypatch):
    test_resp_payload = {
        "username": "user_test",
        "call_count": 10,
        "call_block": 30
    }

    
    def mock_get(key, rdb):
        return json.dumps(test_resp_payload)

    monkeypatch.setattr(redis_op, "get", mock_get)
    

    response = test_app.get('/api/v1/mobile/user_test/billing')

    assert response.status_code == 200
    assert response.json() == test_resp_payload


def test_read_billing_info_not_found(test_app, monkeypatch):
    async def mock_get_billing_info(username, db):
        return None

    
    def mock_get(key, rdb):
        return None

    monkeypatch.setattr(redis_op, "get", mock_get)
    monkeypatch.setattr(mobile, "get_billing_info", mock_get_billing_info)
    

    response = test_app.get('/api/v1/mobile/user_test/billing')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Billing info for user user_test not found'


def test_read_billing_info_invalid_username(test_app, monkeypatch):
    response = test_app.get('/api/v1/mobile/a-very-long-nameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee/billing')
    assert response.status_code == 422


def test_add_cdr(test_app, monkeypatch):
    test_request_payload = {'call_duration': 10500}
    test_response_payload = {'username': 'manh', 'call_duration': 10500, 'created_at': '2022-09-01T18:33:17.362671'}

    async def mock_add_cdr(cdr, db):
        return {
            '_id': ObjectId(),
            **test_response_payload
        }

    def mock_add_task(*args):
        return None

    monkeypatch.setattr(mobile, "add_cdr", mock_add_cdr)
    monkeypatch.setattr(BackgroundTasks, "add_task", mock_add_task)

    response = test_app.post('/api/v1/mobile/manh/call', data=json.dumps(test_request_payload))

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_add_cdr_invalid_input(test_app):
    normal_request_payload = {'call_duration': 10500}
    response = test_app.post('/api/v1/mobile/a-very-long-nameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee/call', data=json.dumps(normal_request_payload))
    assert response.status_code == 422


    abnormal_request_payload = {'call_duration': -1}
    response = test_app.post('/api/v1/mobile/normal-name/call', data=json.dumps(abnormal_request_payload))
    assert response.status_code == 422
