import re
import datetime
import pytest
import json
import os
import requests
from playwright.sync_api import sync_playwright
from utils.cleanup_utils import delete_old_timestamp_folders
from utils.message_utils import send_teams_message, send_slack_message, send_email_from_config
from utils.allure_report import generate_allure_report, parse_allure_summary

# ------------------ GLOBAL VARIABLES ------------------
browser = None
context = None
page = None
playwright = None
config = {}

delete_old_timestamp_folders("screenshots", days_old=7)
delete_old_timestamp_folders("logs", days_old=7)
delete_old_timestamp_folders("reports", days_old=7)

def pytest_sessionfinish(session, exitstatus):
    print("\n[INFO] Post-suite actions started...")

    # 1. Generate Allure report
    generate_allure_report()

    # 2. Extract summary from generated Allure HTML folder
    summary = parse_allure_summary()
    overall_status = "Fail" if summary.get("failed", 0) > 0 else "Pass"

    # 3. Send Email with inline HTML table and optional attachment
    send_email_from_config(
        allure_summary=summary,
        overall_status=overall_status
    )

    msg = f"Test Suite Completed\nStatus: {overall_status}\nPassed: {summary.get('passed', 0)}, Failed: {summary.get('failed', 0)}, Skipped: {summary.get('skipped', 0)}, Duration: {summary.get('duration', 'N/A')}"
    send_teams_message(msg)
    send_slack_message(msg)

    print("[INFO] Post-suite actions completed.")

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

# ------------------ CLI OPTIONS ------------------
def pytest_addoption(parser):
    parser.addoption("--retries", action="store", default=0)
    parser.addoption("--config", action="store", default="data/config.json")

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
def page():
    global browser, context, page
    config = load_config()
    default_browser = config["browser"]
    default_headless = config["headless"]
    browser = getattr(playwright, default_browser).launch(headless=default_headless, args=[
            "--disable-infobars",
            "--disable-notifications",
            "--start-fullscreen",
            "--no-default-browser-check"
        ]
    )
    context = browser.new_context(accept_downloads=True,
        viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    url = config["environment"]["base_url"]
    page.goto(url)
    yield page
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

RUN_TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
SCREENSHOT_DIR = os.path.join("screenshots", RUN_TIMESTAMP)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Get the result from other hooks
    outcome = yield
    report = outcome.get_result()

    # Take screenshot only if the test has failed in the call phase
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # Sanitize test name to make it safe as a filename
            test_name = re.sub(r'[^a-zA-Z0-9_]+', '_', item.name)
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")

            # Capture screenshot
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n[Screenshot] Saved: {screenshot_path}")
