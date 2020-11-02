import time
import cli_colour_utils as makeup


def sleep(sleep_time=1.5, quite_mode=True):
    if quite_mode:
        time.sleep(sleep_time + 1.5)
    else:
        print(makeup.mockup_text_as_ok_blue(f"processing for {sleep_time} seconds..."))
        time.sleep(sleep_time)
