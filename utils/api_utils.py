import requests
import json
from jsonschema import validate, ValidationError

def get(url, headers=None, auth=None, params=None):
    try:
        response = requests.get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] GET request failed: {str(e)}")

def post(url, data=None, json_data=None, headers=None, auth=None):
    try:
        response = requests.post(url, data=data, json=json_data, headers=headers, auth=auth)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] POST request failed: {str(e)}")

def assert_status_code(response, expected_code):
    actual_code = response.status_code
    assert actual_code == expected_code, f"[FAIL] Expected {expected_code}, got {actual_code}"
    print(f"[PASS] Status code is {expected_code}")

def assert_json_key_value(response, key, expected_value):
    try:
        value = response.json().get(key)
        assert value == expected_value, f"[FAIL] Key '{key}' expected '{expected_value}', got '{value}'"
        print(f"[PASS] Key '{key}' has expected value '{expected_value}'")
    except Exception as e:
        raise AssertionError(f"[ERROR] Failed to assert key '{key}': {str(e)}")

def assert_json_contains_keys(response, keys):
    json_data = response.json()
    missing = [key for key in keys if key not in json_data]
    assert not missing, f"[FAIL] Missing keys in response: {missing}"
    print(f"[PASS] All keys {keys} present in response")

def validate_json_schema(response, schema_path):
    try:
        with open(schema_path, 'r') as file:
            schema = json.load(file)
        validate(instance=response.json(), schema=schema)
        print(f"[PASS] JSON matches schema.")
    except ValidationError as e:
        raise AssertionError(f"[FAIL] JSON schema validation error: {e.message}")
    except Exception as e:
        raise Exception(f"[ERROR] Failed to validate schema: {str(e)}")

def get_bearer_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def get_basic_auth(username, password):
    return requests.auth.HTTPBasicAuth(username, password)
