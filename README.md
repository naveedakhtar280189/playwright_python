# Playwright Automation Framework (Web + API)

This is a modular Python-based test automation framework using **Playwright** for web UI and **Requests** for API automation. The design follows best practices such as Page Object Model (POM), reusable components, structured test data, and configuration-driven execution.

---

## ✅ Features

- 🧪 UI Automation with Playwright
- 🔗 API Automation using `requests`
- 📄 Page Object Model with locators and reusable components
- 🧰 Central config (`config.json`) to manage settings and environments
- 🧪 Test data in JSON files
- ♻️ Fixtures for setup, teardown, and shared contexts
- 🔁 Retry support via CLI and hooks
- 📦 Scalable for integration with Allure, DB, Slack, Email, and more

---

## 🗂 Folder Structure

```
.
├── pages/               # Page classes and components
├── locators/            # Locator-only files (decoupled from logic)
├── testdata/            # Input test data in JSON
├── tests/               # All test cases
├── framework_config.json# Centralized config
├── conftest.py          # Pytest hooks, setup, teardown
├── context_fixtures.py  # Reusable fixture combining UI + API
└── framework/
    └── imports.py       # Central import file for all pages and locators
```

---

## 🚀 How to Run

### Install dependencies
```bash
pip install -r requirements.txt
playwright install
```

### Run UI Test
```bash
pytest tests/ --browser=chromium
```

### With Allure Reporting (optional)
```bash
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

### HTML Reporting
pytest --html=reports/test_report.html --self-contained-html .\tests
---

## 🔧 Configurable Settings

Located in `config.json`:
- Base URLs
- Browser selection
- Retry counts
- SMTP / Slack / Teams / DB credentials

---

## 📬 Test Data Usage

```python
with open("testdata/login_data.json") as f:
    data = json.load(f)
```

---

## 🤝 Contributing

Open to collaboration for:
- Mobile extension via Appium
- Reporting plugins
- Jenkins/Azure pipeline YAMLs