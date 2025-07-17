# imports.py - central hub for all reusable classes

# Pages

from page_objects.pages.login_pages.login_page import LoginPage
from components.pages.header_components.header_component import HeaderComponent

# Locators
from page_objects.locators.login_locators.login_locators import LoginLocators
from components.locators.header_locators.header_component import HeaderLocators

# You can import test data via loader, e.g., utils/test_data_loader.py
# or access it in your test like:
# import json; json.load(open("testdata/login_data.json"))

# Example: Configuration can be loaded globally in conftest.py
# You can also add this line if you need:
# from config.framework_config import config  ← if you convert your JSON to Python

# If you use utility classes (email, logging, API), import here too
# from utils.email_utils import EmailSender
# from utils.api_utils import APIClient

# Export for wildcard *
__all__ = [
    "LoginPage", "HeaderComponent",
    "LoginLocators", "HeaderLocators"
]
