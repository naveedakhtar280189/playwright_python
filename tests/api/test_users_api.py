import pytest
from utils.api_utils import (
    send_request,
    get_bearer_headers,
    get_basic_auth,
    assert_status_code,
    assert_json_key_value,
    assert_json_contains_keys,
    validate_json_schema,
    assert_response_time
)

BASE_URL = "https://reqres.in/api"

@pytest.fixture
def token():
    # Normally you fetch this from a login endpoint or env
    return "mocked-jwt-token"

@pytest.fixture
def auth_header(token):
    return get_bearer_headers(token)


def test_get_users_status(auth_header):
    response = send_request("GET", f"{BASE_URL}/users?page=2", headers=auth_header)
    assert_status_code(response, 200)
    assert_json_contains_keys(response, ["page", "data"])


def test_post_create_user(auth_header):
    payload = {"name": "Naveed", "job": "QA Manager"}
    response = send_request("POST", f"{BASE_URL}/users", headers=auth_header, json=payload)
    assert_status_code(response, 201)
    assert_json_key_value(response, "name", "Naveed")
    assert_json_key_value(response, "job", "QA Manager")
    assert_json_contains_keys(response, ["id", "createdAt"])


def test_put_update_user(auth_header):
    payload = {"name": "Naveed", "job": "Director"}
    response = send_request("PUT", f"{BASE_URL}/users/2", headers=auth_header, json=payload)
    assert_status_code(response, 200)
    assert_json_key_value(response, "name", "Naveed")
    assert_json_key_value(response, "job", "Director")


def test_delete_user(auth_header):
    response = send_request("DELETE", f"{BASE_URL}/users/2", headers=auth_header)
    assert_status_code(response, 204)
    assert response.text == ""


def test_basic_auth_request():
    url = "https://httpbin.org/basic-auth/user/passwd"
    response = send_request("GET", url, auth=get_basic_auth("user", "passwd"))
    assert_status_code(response, 200)
    assert_json_key_value(response, "authenticated", True)


def test_validate_schema(auth_header):
    expected_schema = {
        "type": "object",
        "properties": {
            "page": {"type": "integer"},
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                        "email": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "avatar": {"type": "string"},
                    },
                    "required": ["id", "email", "first_name", "last_name", "avatar"]
                }
            }
        },
        "required": ["data"]
    }

    response = send_request("GET", f"{BASE_URL}/users?page=2", headers=auth_header)
    assert_status_code(response, 200)
    validate_json_schema(response, expected_schema)


def test_response_time(auth_header):
    response = send_request("GET", f"{BASE_URL}/users?page=1", headers=auth_header)
    assert_response_time(response, threshold_seconds=2)


# Chained tests with ID passing
user_id_storage = {}

@pytest.mark.dependency(name="create_user")
def test_create_user_return_id(auth_header):
    payload = {"name": "Jane", "job": "QA Lead"}
    response = send_request("POST", f"{BASE_URL}/users", headers=auth_header, json=payload)
    assert_status_code(response, 201)
    user_id = response.json()["id"]
    user_id_storage["id"] = user_id


@pytest.mark.dependency(depends=["create_user"])
def test_get_user_by_id(auth_header):
    user_id = user_id_storage.get("id")
    if not user_id:
        pytest.skip("User ID not available from previous test")
    response = send_request("GET", f"{BASE_URL}/users/{user_id}", headers=auth_header)
    # Note: reqres returns dummy data; the user might not exist, still check for 200 or 404
    assert response.status_code in [200, 404]


@pytest.mark.parametrize("page", [1, 2, 3])
def test_parametrized_user_pages(auth_header, page):
    response = send_request("GET", f"{BASE_URL}/users?page={page}", headers=auth_header)
    assert_status_code(response, 200)
    assert "data" in response.json()
