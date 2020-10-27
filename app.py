from main import open_mp3_juices
import cli_colour_utils as makeup


def normal_entry_point():
    is_app_running = True
    while is_app_running:
        prompt = makeup.mockup_text_as_bold_white('Please enter an song or an artist or type exit: ')
        if (phrase := input(prompt)).lower() == "exit":
            is_app_running = False
        else:
            meta = open_mp3_juices(phrase)
            is_app_running = meta.get("is_app_running")
    else:
        print(makeup.mockup_text_as_ok_blue("have a nice day..."))


if __name__ == '__main__':
    normal_entry_point()
