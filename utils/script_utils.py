import time
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
from datetime import datetime

def find_element(page: Page, selector: str):
    try:
        element = page.query_selector(selector)
        print(f"[{datetime.now()}] Found element: {selector}")
        return element
    except Exception as e:
        print(f"[{datetime.now()}] Error in find_element: {str(e)}")
        return None

def find_elements(page: Page, selector: str):
    try:
        elements = page.query_selector_all(selector)
        print(f"[{datetime.now()}] Found {len(elements)} elements for: {selector}")
        return elements
    except Exception as e:
        print(f"[{datetime.now()}] Error in find_elements: {str(e)}")
        return []

def find_child_element(parent_element, child_selector: str):
    try:
        child = parent_element.query_selector(child_selector)
        print(f"[{datetime.now()}] Found child element: {child_selector}")
        return child
    except Exception as e:
        print(f"[{datetime.now()}] Error in find_child_element: {str(e)}")
        return None

def click_element(page: Page, selector: str):
    try:
        page.click(selector)
        print(f"[{datetime.now()}] Clicked element: {selector}")
    except Exception as e:
        print(f"[{datetime.now()}] Error in click_element: {str(e)}")

def send_keys(page: Page, selector: str, text: str):
    try:
        page.fill(selector, text)
        print(f"[{datetime.now()}] Entered text in element: {selector}")
    except Exception as e:
        print(f"[{datetime.now()}] Error in send_keys: {str(e)}")

def get_text(page: Page, selector: str):
    try:
        text = page.text_content(selector)
        print(f"[{datetime.now()}] Text from element {selector}: {text}")
        return text
    except Exception as e:
        print(f"[{datetime.now()}] Error in get_text: {str(e)}")
        return None

def get_attribute(page: Page, selector: str, attribute_name: str):
    try:
        attr = page.get_attribute(selector, attribute_name)
        print(f"[{datetime.now()}] Attribute '{attribute_name}' from {selector}: {attr}")
        return attr
    except Exception as e:
        print(f"[{datetime.now()}] Error in get_attribute: {str(e)}")
        return None

def press_key(page: Page, selector: str, key: str):
    try:
        page.press(selector, key)
        print(f"[{datetime.now()}] Pressed key '{key}' on element: {selector}")
    except Exception as e:
        print(f"[{datetime.now()}] Error in press_key: {str(e)}")

def accept_alert(page: Page):
    try:
        page.once("dialog", lambda dialog: dialog.accept())
        print(f"[{datetime.now()}] Alert accepted")
    except Exception as e:
        print(f"[{datetime.now()}] Error in accept_alert: {str(e)}")

def dismiss_alert(page: Page):
    try:
        page.once("dialog", lambda dialog: dialog.dismiss())
        print(f"[{datetime.now()}] Alert dismissed")
    except Exception as e:
        print(f"[{datetime.now()}] Error in dismiss_alert: {str(e)}")

def get_window_handles(context):
    try:
        pages = context.pages
        print(f"[{datetime.now()}] Open windows count: {len(pages)}")
        return pages
    except Exception as e:
        print(f"[{datetime.now()}] Error in get_window_handles: {str(e)}")
        return []

def switch_to_window(context, index: int):
    try:
        pages = context.pages
        page = pages[index]
        page.bring_to_front()
        print(f"[{datetime.now()}] Switched to window at index: {index}")
        return page
    except Exception as e:
        print(f"[{datetime.now()}] Error in switch_to_window: {str(e)}")
        return None
    
def select_dropdown(page: Page, selector: str, value: str = None, label: str = None):
    try:
        if value:
            page.select_option(selector, value=value)
            print(f"[{datetime.now()}] Selected value '{value}' from dropdown: {selector}")
        elif label:
            page.select_option(selector, label=label)
            print(f"[{datetime.now()}] Selected label '{label}' from dropdown: {selector}")
    except Exception as e:
        print(f"[{datetime.now()}] Error in select_dropdown: {str(e)}")

def select_custom_dropdown(page: Page, dropdown_selector: str, option_text: str):
    try:
        page.click(dropdown_selector)
        page.click(f"text={option_text}")
        print(f"[{datetime.now()}] Selected '{option_text}' from custom dropdown: {dropdown_selector}")
    except Exception as e:
        print(f"[{datetime.now()}] Error in select_custom_dropdown: {str(e)}")

def pick_date_with_input(page: Page, selector: str, date_str: str):
    try:
        page.fill(selector, "")  # Clear input
        page.fill(selector, date_str)
        print(f"[{datetime.now()}] Entered date '{date_str}' in field: {selector}")
    except Exception as e:
        print(f"[{datetime.now()}] Error in pick_date_with_input: {str(e)}")

def pick_date_from_calendar(page: Page, calendar_open_selector: str, month_selector: str,
                             next_button_selector: str, date_selector_template: str, target_date: str):
    try:
        target = datetime.strptime(target_date, "%Y-%m-%d")
        page.click(calendar_open_selector)

        # Loop until correct month is visible
        while True:
            visible_month = page.inner_text(month_selector)
            if target.strftime("%B %Y") in visible_month:
                break
            page.click(next_button_selector)

        # Click specific date
        page.click(date_selector_template.format(date=target_date))
        print(f"[{datetime.now()}] Selected date '{target_date}' from calendar")
    except Exception as e:
        print(f"[{datetime.now()}] Error in pick_date_from_calendar: {str(e)}")

def js_click(page, selector):
    try:
        page.evaluate("""(sel) => {
            document.querySelector(sel).click();
        }""", selector)
        print(f"[{datetime.now()}] JavaScript click on: {selector}")
    except Exception as e:
        print(f"[{datetime.now()}] JS click failed on {selector}: {str(e)}")

def scroll_into_view(page, selector):
    try:
        page.evaluate("""(sel) => {
            document.querySelector(sel).scrollIntoView({behavior: 'smooth', block: 'center'});
        }""", selector)
        print(f"[{datetime.now()}] Scrolled to element: {selector}")
    except Exception as e:
        print(f"[{datetime.now()}] Scroll failed on {selector}: {str(e)}")

def js_get_value(page, selector):
    try:
        value = page.evaluate("""(sel) => {
            return document.querySelector(sel).value;
        }""", selector)
        print(f"[{datetime.now()}] Value from {selector}: {value}")
        return value
    except Exception as e:
        print(f"[{datetime.now()}] JS get value failed on {selector}: {str(e)}")
        return None
    
def assert_equal(actual, expected, message='Values do not match'):
    try:
        assert actual == expected, f"{message}: Expected '{expected}', got '{actual}'"
        print(f"[PASS] assert_equal: {actual} == {expected}")
    except AssertionError as e:
        print(f"[FAIL] {str(e)}")
        raise

def assert_true(condition, message='Condition is not true'):
    try:
        assert condition, message
        print(f"[PASS] assert_true: Condition met")
    except AssertionError as e:
        print(f"[FAIL] {str(e)}")
        raise

def assert_element_present(page, selector, message="Element not found"):
    try:
        element = page.query_selector(selector)
        assert element is not None, message
        print(f"[PASS] Element found: {selector}")
    except Exception as e:
        print(f"[FAIL] assert_element_present: {str(e)}")
        raise

def assert_element_visible(page, selector, message="Element not visible"):
    try:
        visible = page.is_visible(selector)
        assert visible, message
        print(f"[PASS] Element visible: {selector}")
    except Exception as e:
        print(f"[FAIL] assert_element_visible: {str(e)}")
        raise

def assert_text_in_element(page, selector, expected_text, message="Text not found in element"):
    try:
        actual_text = page.inner_text(selector)
        assert expected_text in actual_text, f"{message}: Expected '{expected_text}' in '{actual_text}'"
        print(f"[PASS] Text found in element: '{expected_text}' in '{actual_text}'")
    except Exception as e:
        print(f"[FAIL] assert_text_in_element: {str(e)}")
        raise

def wait_for_element_visible(page: Page, selector: str, timeout: int = 5000):
    """
    Wait for an element to become visible using Playwright's explicit wait.
    """
    try:
        page.locator(selector).wait_for(state="visible", timeout=timeout)
        print(f"[PASS] Element is visible: {selector}")
    except PlaywrightTimeoutError:
        print(f"[FAIL] Element not visible after {timeout}ms: {selector}")
        raise

def wait_for_selector_with_timeout(page: Page, selector: str, timeout: int = 5000):
    """
    Wait for a selector to appear in the DOM.
    """
    try:
        page.wait_for_selector(selector, timeout=timeout)
        print(f"[PASS] Selector found: {selector}")
    except PlaywrightTimeoutError:
        print(f"[FAIL] Selector not found after {timeout}ms: {selector}")
        raise

def fluent_wait(page: Page, selector: str, timeout: int = 10, poll_interval: float = 0.5):
    """
    Custom polling logic to check element visibility, similar to Selenium FluentWait.
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            if page.is_visible(selector):
                print(f"[PASS] Element became visible: {selector}")
                return True
        except:
            pass
        time.sleep(poll_interval)
    raise TimeoutError(f"[FAIL] Element not visible after {timeout} seconds: {selector}")

def wait_with_sleep_check(condition_func, timeout: int = 10, poll_interval: float = 1):
    """
    Wait for any boolean condition with polling.
    Usage: wait_with_sleep_check(lambda: page.is_visible("#id"))
    """
    end = time.time() + timeout
    while time.time() < end:
        if condition_func():
            print("[PASS] Condition met.")
            return
        time.sleep(poll_interval)
    raise TimeoutError("[FAIL] Condition not met within timeout.")
