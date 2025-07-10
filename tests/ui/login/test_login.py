import json
from imports.imports import LoginPage 
import conftest

def load_test_data():
    with open("testdata/login_data.json") as f:
        return json.load(f)

def test_valid_login(setup):
    page = setup
    data = load_test_data()
    login_data = data["valid_user"]
    login_page = LoginPage(page)
    login_page.login(login_data["username"], login_data["password"])
    page.go(conftest.base_url)
    assert "dashboard" in page.url
