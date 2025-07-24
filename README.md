# 🧪 Playwright + Pytest Automation Framework (Python)

This is a modern, scalable **Python automation framework** using **Playwright** and **Pytest**, designed for UI and API testing with built-in support for:

- 🔄 Parallel & cross-browser execution  
- 📊 Reporting via Allure  
- 🖼️ Screenshot on failure  
- 📤 Notifications (Email, Slack, Teams)  
- 🛠 Health checks  
- 🧹 Periodic cleanup  
- 📁 Multi-environment support via config files  

---

## 🛠 Framework Overview

| Feature                   | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| **Framework**             | Custom-built using `pytest`, `playwright`                                   |
| **Language**              | Python 3.8+                                                                 |
| **Test Types**            | UI (via Playwright), API (via requests)                                     |
| **Browsers Supported**    | Chromium, Firefox, WebKit                                                   |
| **Parallel Execution**    | Yes – via `pytest-xdist`                                                    |
| **Retry Logic**           | Yes – via `--retries` (manual, extendable with `pytest-rerunfailures`)      |
| **Reports**               | Allure (with optional HTML, CLI)                                            |
| **CI/CD Ready**           | ✅ Fully customizable for Jenkins, GitHub Actions, GitLab, etc.              |

---

## 📁 Folder Structure

```
project/
├── conftest.py                    # Core logic: CLI, fixtures, setup, teardown
├── data/
│   └── config.json                # Environment, browser & auth config
├── tests/
│   ├── test_ui_sample.py         # Sample UI test
│   └── test_api_sample.py        # Sample API test
├── utils/
│   ├── allure_report.py          # Allure report generation & summary
│   ├── cleanup_utils.py          # Folder cleanup logic
│   ├── health_check.py           # App/API/DB health validations
│   └── message_utils.py          # Email, Slack, Teams messaging
├── screenshots/                  # Screenshots on failure (timestamped)
├── reports/                      # Allure report output
├── logs/                         # Optional logging support
├── allure-results/               # Allure raw result files
├── requirements.txt              # Python dependency list
└── README.md                     # You're here
```

---

## 🧪 Sample Tests

### ✅ UI Test: `test_ui_sample.py`

```python
def test_open_google(page):
    page.goto("https://www.google.com")
    assert "Google" in page.title()
```

### ✅ API Test: `test_api_sample.py`

```python
def test_api_get_user(api_session):
    response = api_session.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

---

## ⚙️ Configuration

Update `data/config.json`:

```json
{
  "browser": "chromium",
  "headless": true,
  "environment": {
    "base_url": "https://example.com",
    "auth_token_env_var": "AUTH_TOKEN"
  }
}
```

🔒 Set token securely using environment variable:
```bash
export AUTH_TOKEN="your-token"
```

---

## 🧼 Auto Cleanup

The framework automatically deletes folders older than 7 days from:

- `screenshots/`
- `logs/`
- `reports/`
- `allure-results/`

Controlled via `delete_old_timestamp_folders()` in `conftest.py`.

---

## 📸 Screenshot on Failure

On test failure, full-page screenshot is saved at:

```
screenshots/<timestamp>/<testname>.png
```

---

## 📤 Notifications (Optional)

Enable and configure in `conftest.py`:

- Email via `send_email_from_config()`
- Slack via `send_slack_message()`
- Teams via `send_teams_message()`

---

## 📊 Allure Reporting

### ✅ Generate (Automatically Done in `conftest.py`)
```bash
allure generate allure-results/ -o reports/allure-report --clean
```

### ✅ Serve locally
```bash
allure serve allure-results/
```

---

## 🧪 Test Execution Commands

### ✅ 1. Run Single Browser, Single Instance

```bash
pytest --browsers=chromium --instances=1
```

---

### ✅ 2. Run Single Browser, Multiple Instances (Parallel)

```bash
pytest -n 4 --browsers=chromium --instances=4
```

---

### ✅ 3. Run Multiple Browsers (Parallel Across All)

```bash
pytest -n auto --browsers=chromium,firefox,webkit --instances=2
```

---

### ✅ 4. Run with Config Override

```bash
pytest --config=data/staging_config.json
```

---

### ✅ 5. Run with Manual Retry (via rerunfailures plugin)

```bash
pip install pytest-rerunfailures
pytest --reruns=2 --browsers=chromium --instances=2
```

> Alternatively, you can implement retry logic inside `conftest.py` via `--retries` (manual control).

---

## 🧩 CLI Options

| Option            | Default            | Description                                     |
|-------------------|--------------------|-------------------------------------------------|
| `--browsers`       | `chromium`         | Comma-separated list: chromium,firefox,webkit   |
| `--instances`      | `1`                | Number of instances per browser                 |
| `--config`         | `data/config.json` | Path to config file                             |
| `--retries`        | `0`                | Retry logic (manually controlled)               |

---

## 📦 Requirements

Create a `requirements.txt` with:

```
pytest
pytest-xdist
pytest-playwright
requests
allure-pytest
pytest-rerunfailures
```

Install with:

```bash
pip install -r requirements.txt
playwright install
```

---

## 🚦 Health Checks (Optional)

Enable in `conftest.py`:
```python
@pytest.fixture(scope="session", autouse=True)
def run_health_checks_before_suite():
    ...
```

Checks:
- Web app reachable
- API alive
- DB connection
- Mobile backend alive

Fails test run if any system is down.

---

## 🧬 Extendability

You can extend the framework to:
- Run tagged or grouped tests (`pytest -m smoke`)
- Use data-driven tests via `@pytest.mark.parametrize`
- Include visual testing tools (e.g. Percy)
- Integrate with CI/CD (Jenkins, GitHub Actions, GitLab)

---

## 🤝 Contributing

Pull requests and feedback are welcome. Fork the repo, create a feature branch, and submit a PR.

---

## 📧 Need Help?

Open an issue or contact the maintainer if you'd like help scaling or integrating this with CI/CD pipelines.

---

**Happy Testing! 🚀**