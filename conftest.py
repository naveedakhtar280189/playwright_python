import pytest
import json
import os
import requests
from playwright.sync_api import sync_playwright
import logging

# ------------------ GLOBAL VARIABLES ------------------
browser = None
context = None
page = None
playwright = None
config = {}

# ------------------ CONFIG LOADER ------------------
def load_config(path='data/config.json'):
    with open(path, 'r') as f:
        cfg = json.load(f)
    env_section = cfg.get("environment", {})
    
    # Overwrite password/tokens with env var if set
    if env_section.get("auth_token_env_var"):
        env_token = os.getenv(env_section["auth_token_env_var"])
        if env_token:
            env_section["auth_token"] = env_token

    cfg["environment"] = env_section
    return cfg

@pytest.fixture
def base_url():
    return load_config["environment"]["base_url"]

# ------------------ CLI OPTIONS ------------------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chromium")
    parser.addoption("--retries", action="store", default=0)
    parser.addoption("--config", action="store", default="framework_config.json")

# ------------------ SUITE LEVEL SETUP ------------------
@pytest.fixture(scope="session", autouse=True)
def before_suite(request):
    global playwright, config
    config_path = request.config.getoption("--config")
    config = load_config(config_path)

    print("\n[BeforeSuite] Starting Playwright")
    playwright = sync_playwright().start()
    yield
    print("\n[AfterSuite] Stopping Playwright")
    playwright.stop()

# ------------------ PER TEST SETUP ------------------
@pytest.fixture(scope="function")
def setup(request):
    global browser, context, page
    browser_name = request.config.getoption("--browser")
    browser = getattr(playwright, browser_name).launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.goto()
    page.close()
    context.close()
    browser.close()

# ------------------ API SESSION FIXTURE ------------------
@pytest.fixture(scope="function")
def api_session():
    session = requests.Session()
    headers = {
        "Content-Type": "application/json"
    }
    token = config.get("environment", {}).get("auth_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    session.headers.update(headers)
    return session

# ------------------ RETRY HOOK ------------------
def pytest_runtest_call(item):
    max_retries = int(item.config.getoption("--retries", 0))
    retry_count_marker = item.get_closest_marker("retry_count")
    if retry_count_marker:
        max_retries = int(retry_count_marker.args[0])

    for attempt in range(max_retries + 1):
        try:
            item.runtest()
            return
        except Exception as e:
            if attempt < max_retries:
                logging.warning(f"[RETRY] {item.name} failed. Retrying {attempt + 1}/{max_retries}...")
            else:
                raise
