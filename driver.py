import os
from selenium import webdriver


def get_browser(do_not_show_browser=True):
    setup_options = webdriver.ChromeOptions()
    setup_options.headless = do_not_show_browser
    setup_options.add_argument('--no-sandbox')
    setup_options.add_argument('--disable-dev-shm-usage')
    chrome_driver_path = os.path.join(os.path.abspath('.'), "chromedriver")
    return webdriver.Chrome(chrome_driver_path, options=setup_options)


def get_element_child_count(element):
    return 0 if element is None else int(element.get_attribute("childElementCount"))


def get_xpath(tag, attribute, value):
    return f'//{tag}[@{attribute}="{value}"]'
