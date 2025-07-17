from page_objects.pages.login_pages.login_page import LoginPage
from utils.config_reader import read_json_config

def test_valid_login(page):
    
    login_page = LoginPage(page)
    username, password = login_page.get_valid_login_credentials()
    login_page.login(username, password)

