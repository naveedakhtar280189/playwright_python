import pytest
import os
import json
import datetime
import re
import requests
from playwright.sync_api import sync_playwright
from utils.cleanup_utils import delete_old_timestamp_folders
from utils.message_utils import send_teams_message, send_slack_message, send_email_from_config
from utils.allure_report import generate_allure_report, parse_allure_summary
from utils.health_check import check_api, check_web_app, check_mobile_backend, check_database

# ------------------ CLEANUP OLD FILES ------------------ #
for folder in ["screenshots", "logs", "reports", "allure-results"]:
    delete_old_timestamp_folders(folder, days_old=7)

# ------------------ GLOBALS ------------------ #
RUN_TIMESTAMP = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
SCREENSHOT_DIR = os.path.join("screenshots", RUN_TIMESTAMP)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

config = {}
playwright = None

# ------------------ CLI OPTIONS ------------------ #
def pytest_addoption(parser):
    parser.addoption("--config", action="store", default="data/config.json")
    parser.addoption("--browsers", action="store", default="chromium", help="Comma-separated: chromium,firefox,webkit")
    parser.addoption("--instances", action="store", default="1", help="Instances per browser")
    parser.addoption("--mcp", action="store_true", help="Enable MCP (Model Component Proxy) for self-healing")

# ------------------ LOAD CONFIG ------------------ #
def load_config(path='data/config.json'):
    with open(path, 'r') as f:
        cfg = json.load(f)
    env_section = cfg.get("environment", {})
    token_var = env_section.get("auth_token_env_var")
    if token_var:
        token = os.getenv(token_var)
        if token:
            env_section["auth_token"] = token
    cfg["environment"] = env_section
    return cfg

# ------------------ PARAMETRIZE TESTS ------------------ #
def pytest_generate_tests(metafunc):
    browsers = metafunc.config.getoption("browsers").split(",")
    instances = int(metafunc.config.getoption("instances"))
    params = [(browser.strip(), i) for browser in browsers for i in range(instances)]
    if "browser_instance" in metafunc.fixturenames:
        metafunc.parametrize("browser_instance", params)

# ------------------ SUITE STARTUP ------------------ #
@pytest.fixture(scope="session", autouse=True)
def before_suite(request):
    global playwright, config
    config = load_config(request.config.getoption("--config"))
    print("\n[Setup] Starting Playwright...")
    playwright = sync_playwright().start()
    yield
    print("\n[Teardown] Stopping Playwright...")
    playwright.stop()

# ------------------ PAGE FIXTURE ------------------ #
@pytest.fixture
def page(browser_instance):
    browser_name, _ = browser_instance
    default_headless = config.get("headless", True)
    mcp_enabled = config.get("enable_mcp", False)
    proxy_config = {"server": config.get("mcp_proxy", "http://localhost:3000")} if mcp_enabled else None

    args = [
        "--disable-infobars", "--disable-notifications", "--start-fullscreen",
        "--no-default-browser-check"
    ]
    if mcp_enabled:
        args.append("--proxy-server=http://localhost:3000")

    launch_options = {
        "headless": default_headless,
        "args": args,
    }
    if proxy_config:
        launch_options["proxy"] = proxy_config

    browser = getattr(playwright, browser_name).launch(**launch_options)
    context = browser.new_context(accept_downloads=True, viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto(config["environment"]["base_url"])

    yield page

    page.close()
    context.close()
    browser.close()

# ------------------ API SESSION FIXTURE ------------------ #
@pytest.fixture
def api_session():
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    token = config.get("environment", {}).get("auth_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    session.headers.update(headers)
    return session

# ------------------ SCREENSHOT ON FAILURE ------------------ #

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Only act after the test "call" phase and if it failed
    if report.when == "call" and report.failed:
        # Try to get the Playwright page object (may not exist for API tests)
        page = item.funcargs.get("page", None)

        if page and hasattr(page, "screenshot"):
            try:
                test_name = re.sub(r'[^a-zA-Z0-9_]+', '_', item.name)
                screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"\n[Screenshot] Saved: {screenshot_path}")
            except Exception as e:
                print(f"[WARN] Screenshot capture failed: {e}")
        else:
            print(f"[INFO] No Playwright page object — skipping screenshot for: {item.name}")
# ------------------ POST-SUITE ACTIONS ------------------ #
def pytest_sessionfinish(session, exitstatus):
    print("\n[Post-Suite] Generating Allure report...")
    generate_allure_report()
    summary = parse_allure_summary()
    overall_status = "Fail" if summary.get("failed", 0) > 0 else "Pass"

    # Uncomment to enable notifications
    # send_email_from_config(allure_summary=summary, overall_status=overall_status)
    # msg = f"Test Suite Completed\nStatus: {overall_status}\nPassed: {summary.get('passed', 0)}, Failed: {summary.get('failed', 0)}, Skipped: {summary.get('skipped', 0)}, Duration: {summary.get('duration', 'N/A')}"
    # send_teams_message(msg)
    # send_slack_message(msg)

    print("[Post-Suite] Allure and notifications complete.")