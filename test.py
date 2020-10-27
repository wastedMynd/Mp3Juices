from main import characters_to_replace, get_file_name, get_range_selection_list, get_specific_selection_list, \
    get_browser, mp3_juices_url
from unittest import TestCase
import re


class TestApp(TestCase):
    def test_get_web_driver(self):
        with get_browser(do_not_show_browser=True) as driver:
            self.assertIsNotNone(driver)
            driver.get(url=mp3_juices_url)
            actual_title = driver.title
            self.assertIsNotNone(actual_title)
            self.assertEqual(actual_title, "MP3Juices - Free MP3 Downloads")

    def test_file_name_do_not_contain_invalid_chars(self):
        title = "#my$ong%nyc.mp3"
        result = get_file_name(title)

        def iter_over_characters_to_replace(test_case, operation, expected):
            for char in characters_to_replace:
                test_case(operation(char), expected)

        def validate_invalid_char_and_getfilename(char):
            if char in result:
                raise AssertionError(f"{char} found!")
            return result

        iter_over_characters_to_replace(
            self.assertEqual,
            operation=validate_invalid_char_and_getfilename,
            expected="my ong nyc mp3"
        )

    def test_single_entry_selection_re(self):
        selection = "100"

        def get_single_entry_selection_match(selected: str = None):
            if selected is None:
                raise AssertionError("please provide a selection!")

            re_pattern = r'(\d+)'
            return re.match(re_pattern, selected).group(1)

        self.assertEqual(get_single_entry_selection_match(selection), selection)

    def test_range_entry_selection_re(self):
        def get_range_entry_selection_split(selected: str = None):
            if selected is None:
                raise AssertionError("please provide a range selection!")

            return selected \
                .strip() \
                .replace('[', '').replace(']', '') \
                .replace('(', '').replace(')', '') \
                .replace('{', '').replace('}', '') \
                .replace(' ', '').split('-')

        selections = [
            "10-15", " 10-15", "10 -15", "10- 15", "10-15 ", "  10 -  15 ",  # range with spaces and without brackets
            "[10-15]", "[ 10-15]", "[10 -15]", "[10- 15]", "[10-15 ]", "[ 10 - 15 ]",  # range with brackets and spaces
            "[10-15", "[ 10-15", "[10 -15", "[10- 15", "[10-15 ", "[ 10 - 15       ",  # range with a bracket and spaces
            "10-15]", " 10-15]", "10 -15]", "10- 15]", "10-15 ]", " 10 - 15        ]"  # range with a bracket and spaces
        ]
        for selection in selections:
            self.assertEqual(
                get_range_selection_list(selection),
                get_range_entry_selection_split(selection)
            )

    def test_specific_entry_selection_re(self):
        def get_entry_selection_split(selected: str = None):
            if selected is None:
                raise AssertionError("please provide a range selection!")

            selected = selected[:len(selected) - 1] if selected.endswith(',') else selected

            return selected \
                .strip() \
                .replace('[', '').replace(']', '') \
                .replace('(', '').replace(')', '') \
                .replace('{', '').replace('}', '') \
                .replace(' ', '').split(',')

        selections = [
            "10,15", " 10,15", "10 ,15", "10, 15", "10,15 ", "  10 ,  15 ",  # range with spaces and without brackets
            "[10,15]", "[ 10,15]", "[10 ,15]", "[10, 15]", "[10,15 ]", "[ 10 , 15 ]",  # range with brackets and spaces
            "[10,15", "[ 10,15", "[10 ,15", "[10, 15", "[10,15 ", "[ 10 , 15       ",  # range with a bracket and spaces
            "10,15]", " 10,15]", "10 ,15]", "10, 15]", "10,15 ]", " 10 , 15        ]"  # range with a bracket and spaces
        ]
        for selection in selections:
            self.assertEqual(
                get_specific_selection_list(selection),
                get_entry_selection_split(selection)
            )
