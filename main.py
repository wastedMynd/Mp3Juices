import re

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import cli_colour_utils as makeup
from downloader import initialize_download
from driver import get_browser, get_element_child_count, get_xpath
from utils import sleep
from mp3juices_scrapper import scrape_query_field_and_search_for_query, scrape_submit_search_query_button

mp3_juices_url = 'https://www.mp3juices.cc'


# region selection as : single, all, range, and specific selection region
def get_range_selection_list(selection=None):
    if selection is None:
        return None

    re_pattern = r'(\[)?(\()?(\{)?(\s+)?(\d+)(\s+)?[-](\s+)?(\d+)(\s+)?(\})?(\))?(\])?'
    match = re.match(re_pattern, selection)

    try:
        return [match.group(5), match.group(8)]
    except AttributeError:
        return None


def get_range_selection_as_an_int_list(selection=None):
    if selection is None:
        return []

    range_selection_as_a_str_list = get_range_selection_list(selection)

    if range_selection_as_a_str_list is None:
        return None
    return [int(selection_item) - 1 for selection_item in range_selection_as_a_str_list]


def get_specific_selection_list(selection=None):
    if selection is None:
        return []

    selected = selection[:len(selection) - 1] if selection.endswith(',') else selection

    return selected \
        .strip() \
        .replace('[', '').replace(']', '') \
        .replace('(', '').replace(')', '') \
        .replace('{', '').replace('}', '') \
        .replace(' ', '') \
        .split(',')


def get_specific_selection_as_an_int_list(selection=None):
    if selection is None:
        return []

    specific_selection_as_a_str_list = get_specific_selection_list(selection)
    return [int(selection_item) - 1 for selection_item in specific_selection_as_a_str_list]


def get_single_selection_list(selection= None):
    if selection is None:
        return []

    entry_selection_re = r'(\d+)'
    match = re.match(entry_selection_re, selection)
    return [] if match is None else [match.group(1)]


def get_single_selection_as_an_int_list(selection= None):
    selection_list = get_single_selection_list(selection)
    return [] if len(selection_list) == 0 else [ int(s) - 1 for s in selection_list]


# endregion

def open_mp3_juices(search_query=None, selection_param=None, option_param=None, grouping=None, quite_mode=True):
    """
    returns:
    is_app_running True, response "search query is not provided!"
    is_app_running False, response "Internet connection is down!"
    is_app_running True, response f"query {search_query} can't be found!"
    """

    # validate search_query
    if search_query is None:
        response = "search query is not provided!"
        print(makeup.mockup_text_as_warning_yellow(response))
        return {
            "is_app_running": True,
            "response": response
        }

    # region go to the https://www.mp3juices.cc page
    browser = get_browser()
    browser.get(mp3_juices_url)
    # endregion

    # region scrap the search_input_element and send search_query to search_input_element
    response = scrape_query_field_and_search_for_query(search_query, browser, quite_mode)
    if not response.get("is_app_running"):
        return response
    # endregion

    # region scrap the search_submit_button_element and click on it.
    scrape_submit_search_query_button(search_query, browser, quite_mode)
    # endregion

    is_results_found = False
    results = None
    retry_count = 0

    while not is_results_found:
        sleep(2)
        try:
            results = browser.find_element_by_xpath(get_xpath("div", "id", "results"))
            is_results_found = not (results is None) and get_element_child_count(results) > 0
            if not is_results_found:
                if retry_count == 3:
                    break
                retry_count += 1
            else:
                break
        except NoSuchElementException:
            if not is_results_found:
                if retry_count == 3:
                    break
                retry_count += 1
            continue

    if results is None or not is_results_found:
        print(makeup.mockup_text_as_warning_yellow(response := f"query {search_query} can't be found!"))
        return {
            "is_app_running": True,
            "response": response
        }

    description = results.find_element_by_tag_name("p").text
    for desc in description.split('.'):
        if not quite_mode:
            print(desc.strip())

    mp3_results_count = get_element_child_count(results)

    mp3_results_holder = []
    for mp3_result_index in range(1, mp3_results_count):
        mp3_result = results.find_element_by_id(f"result_{mp3_result_index}")
        mp3_result_result_title = mp3_result.find_element_by_class_name("name").text
        mp3_result_result_properties = mp3_result.find_element_by_class_name("properties").text
        mp3_result_result_options = mp3_result.find_element_by_class_name("options")
        mp3_result_result_option_download = mp3_result_result_options.find_element_by_class_name("download")
        mp3_result_result_option_play = mp3_result_result_options.find_element_by_class_name("player")

        mp3_result_result_properties_meta = mp3_result_result_properties.split('•')
        mp3_result_result_properties_source = mp3_result_result_properties_meta[0].replace("Source:", "").strip()
        mp3_result_result_properties_time = mp3_result_result_properties_meta[1].replace("Time:", "").strip()
        mp3_result_result_properties_bit_rate = mp3_result_result_properties_meta[2].replace("Bitrate:", "").strip()

        mp3_result = {
            "id": mp3_result_index,
            "title": mp3_result_result_title,
            "properties": {
                'source': mp3_result_result_properties_source,
                'grouping': grouping,
                'time': mp3_result_result_properties_time,
                'bit_rate': mp3_result_result_properties_bit_rate
            },
            "options": {
                "download": mp3_result_result_option_download,
                "play": mp3_result_result_option_play
            }
        }
        mp3_results_holder.append(mp3_result)

        if not quite_mode:
            print("{:<2} {:^100} {:<20}".format(
                makeup.mockup_text_as_clear_white(str(mp3_result_index)),
                makeup.mockup_text_as_header_purple(mp3_result_result_title),
                makeup.mockup_text_as_underlined_white(mp3_result_result_properties)
            )
            )

    # prompt user for, mp3 selection
    is_selected_entry_valid = False
    total = len(mp3_results_holder)

    while not is_selected_entry_valid:
        prompt = f"""
        Please select an entry from 1 to {mp3_results_count},
        Or type "All"
        Or specify a range from (1 - {total}),
        Or specify a selective [1, {total}]:
        \n
        """
        selection = input(makeup.mockup_text_as_bold_white(prompt)) if selection_param is None else selection_param

        entry_selected = None

        if re.match(r'(all)', selection.lower()) is not None:
            entry_selected = range(0, total)
            is_selected_entry_valid = True

        elif (selection_list := get_range_selection_as_an_int_list(selection)) is not None:

            minimum = selection_list[0]
            maximum = selection_list[1]

            if minimum < 0 or minimum > total or minimum > maximum:
                print(makeup.mockup_text_as_fail_red("invalid entry selection!"))
                is_selected_entry_valid = False
                continue
            elif maximum < minimum or maximum > total:
                print(makeup.mockup_text_as_fail_red("invalid entry selection!"))
                is_selected_entry_valid = False
                continue

            entry_selected = range(minimum, maximum)
            is_selected_entry_valid = True

        elif (selection_list := get_specific_selection_as_an_int_list(selection)) is not None \
                or (selection_list := get_single_selection_as_an_int_list(selection)) is not None:

            for selection in selection_list:
                if selection < 0 or selection > total:
                    print(makeup.mockup_text_as_fail_red("invalid entry selection!"))
                    is_selected_entry_valid = False
                    break
                else:
                    is_selected_entry_valid = True

            if not is_selected_entry_valid:
                continue

            entry_selected = list(selection_list)

        else:
            print(makeup.mockup_text_as_fail_red("invalid entry selection!"))
            is_selected_entry_valid = False
            continue

        # prompt user to download or play or exit
        prompt = makeup.mockup_text_as_bold_white(
            'Would you like to "download = D", or "play = P"; selection(s) or "exit = E": '
        )
        selected_option = input(prompt).lower() if option_param is None else option_param.lower()
        if selected_option == "e" or not selected_option:
            if not quite_mode:
                print(makeup.mockup_text_as_bold_white('exiting...!'))
            break
        elif selected_option == "d":
            option_type = "download"
            if not quite_mode:
                print(makeup.mockup_text_as_ok_blue(f"{option_type} initialized..."))
            if type(entry_selected) is range or type(entry_selected) is list:
                for entry in entry_selected:
                    try:
                        mp3_results_holder[entry].get("options").get(option_type).click()
                        sleep(30)
                        initialize_download(option_type, results, entry, mp3_results_holder,grouping ,search_query)
                    except ElementClickInterceptedException:
                        mp3_title = mp3_results_holder[entry].get("title")
                        response = f"{makeup.mockup_text_as_header_purple(mp3_title)} " \
                                   f"{makeup.mockup_text_as_fail_red('not downloaded!')}"
                        print(response, end='\n\r')
                        continue
                else:
                    break

        elif selected_option == "p":
            option_type = "play"
            print(makeup.mockup_text_as_warning_yellow(f"{option_type} function not implemented yet..."))
            break
    return {
        "is_app_running": True,
        "response": f"done executing, query {search_query} operation."
    }

# todo family diner , by snarky
