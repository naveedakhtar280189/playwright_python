import requests
import json
import logging
from jsonschema import validate, ValidationError
from requests.auth import HTTPBasicAuth

# Logger configuration
logger = logging.getLogger("api_utils")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# -------------------------------------
# Basic HTTP Methods
# -------------------------------------
def get(url, headers=None, auth=None, params=None):
    try:
        response = requests.get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        logger.info(f"[GET] {url} -> {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] GET request failed: {str(e)}")

def post(url, data=None, json_data=None, headers=None, auth=None):
    try:
        response = requests.post(url, data=data, json=json_data, headers=headers, auth=auth)
        response.raise_for_status()
        logger.info(f"[POST] {url} -> {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] POST request failed: {str(e)}")

def put(url, data=None, json_data=None, headers=None, auth=None):
    try:
        response = requests.put(url, data=data, json=json_data, headers=headers, auth=auth)
        response.raise_for_status()
        logger.info(f"[PUT] {url} -> {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] PUT request failed: {str(e)}")

def delete(url, headers=None, auth=None):
    try:
        response = requests.delete(url, headers=headers, auth=auth)
        logger.info(f"[DELETE] {url} -> {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] DELETE request failed: {str(e)}")

# -------------------------------------
# Unified Request Method
# -------------------------------------
def send_request(method, url, headers=None, params=None, json=None, data=None, auth=None, timeout=10):
    try:
        logger.info(f"Request: [{method}] {url}")
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json,
            data=data,
            auth=auth,
            timeout=timeout
        )
        logger.info(f"Response: {response.status_code}")
        response.raise_for_status()
        return response
    except Exception as e:
        logger.error(f"[ERROR] {method} request failed: {e}")
        raise

# -------------------------------------
# Auth Utilities
# -------------------------------------
def get_bearer_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def get_basic_auth(username, password):
    return HTTPBasicAuth(username, password)

# -------------------------------------
# Assertion Utilities
# -------------------------------------
def assert_status_code(response, expected_code):
    actual_code = response.status_code
    assert actual_code == expected_code, f"[FAIL] Expected {expected_code}, got {actual_code}"
    logger.info(f"[PASS] Status code is {expected_code}")

def assert_json_key_value(response, key, expected_value):
    try:
        value = response.json().get(key)
        assert value == expected_value, f"[FAIL] Key '{key}' expected '{expected_value}', got '{value}'"
        logger.info(f"[PASS] Key '{key}' has expected value '{expected_value}'")
    except Exception as e:
        raise AssertionError(f"[ERROR] Failed to assert key '{key}': {str(e)}")

def assert_json_contains_keys(response, keys):
    json_data = response.json()
    missing = [key for key in keys if key not in json_data]
    assert not missing, f"[FAIL] Missing keys in response: {missing}"
    logger.info(f"[PASS] All keys {keys} present in response")

def validate_json_schema(response, schema_path):
    try:
        with open(schema_path, 'r') as file:
            schema = json.load(file)
        validate(instance=response.json(), schema=schema)
        logger.info(f"[PASS] JSON matches schema.")
    except ValidationError as e:
        raise AssertionError(f"[FAIL] JSON schema validation error: {e.message}")
    except Exception as e:
        raise Exception(f"[ERROR] Failed to validate schema: {str(e)}")

def assert_response_time(response, threshold_seconds=2):
    duration = response.elapsed.total_seconds()
    assert duration < threshold_seconds, f"[FAIL] Response time {duration:.2f}s exceeds {threshold_seconds}s"
    logger.info(f"[PASS] Response time: {duration:.2f}s")
