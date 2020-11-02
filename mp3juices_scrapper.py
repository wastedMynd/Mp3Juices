from driver import get_xpath
import cli_colour_utils as makeup
from utils import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


def scrape_query_field_and_search_for_query(search_query, browser, quite_mode=True) -> dict:
    """ scrape the search_input_element and send search_query to search_input_element """
    try:
        query_element = browser.find_element_by_xpath(get_xpath('input', 'name', 'query'))
        if not quite_mode:
            print(makeup.mockup_text_as_bold_white(f"typing... query {search_query}"))
        query_element.send_keys(search_query)
        sleep(2)
        mockup_response = makeup.mockup_text_as_bold_white(response := "Query found.")
        if not quite_mode:
            print(mockup_response)
        return {
            "is_app_running": True,
            "response": response
        }
    except NoSuchElementException:
        mockup = makeup.mockup_text_as_bold_white(response := "Internet connection is down!")
        print(makeup.mockup_text_as_fail_red(mockup))
        return {
            "is_app_running": False,
            "response": response
        }


def scrape_submit_search_query_button(search_query, browser, quite_mode=True):
    """ scrape the search_submit_button_element and click on it """
    browser.find_element_by_xpath(get_xpath("button", "type", "submit")).click()
    sleep(2)
    if not quite_mode:
        print(makeup.mockup_text_as_bold_white(f"displaying result... query {search_query}"))
    pass
