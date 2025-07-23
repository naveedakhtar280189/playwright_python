from page_objects.locators.login_locators.login_locators import LoginLocators
from utils.script_utils import ScriptUtils
from utils.logger_utils import get_logger 
from utils.config_reader import read_json_config

logger = get_logger()

class LoginPage:
    def __init__(self, page):
        self.page = page
        logger.debug("LoginPage initialized")

    def login(self, username, password):
        try:
            logger.info("Starting login process")
            logger.debug(f"Entering username: {username}")
            self.page.fill(LoginLocators.USERNAME_INPUT, username)

            logger.debug(f"Entering password: {'*' * len(password)}")
            self.page.fill(LoginLocators.PASSWORD_INPUT, password)

            logger.debug("Clicking the login button")
            self.page.click(LoginLocators.LOGIN_BUTTON)

            logger.debug("Waiting for profile icon to appear")
            ScriptUtils.assert_element_visible(self.page, LoginLocators.PROFILE_ICON)

            logger.info("Login successful")

        except Exception as e:
            logger.exception(f"Login failed: {str(e)}")
            raise

    @staticmethod
    def get_valid_login_credentials():
        """
        Loads valid login credentials from JSON config and returns them as a tuple.
        """
        try:
            logger.debug("Reading login data from 'testdata/login_data.json'")
            data = read_json_config("testdata/login_data.json")
            login_data = data["valid_user"]
            username = login_data["username"]
            password = login_data["password"]
            logger.debug("Successfully loaded login credentials")
            return username, password
        except Exception as e:
            logger.exception("Failed to load login credentials")
            raise
