class ForegroundColours:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    CLEAR_WHITE = '\033[0m'
    BOLD = '\033[1m'
    UNDER_LINE = '\033[4m'


def mockup_text_as_warning_yellow(text: str) -> str:
    return f'{ForegroundColours.WARNING} {text} {ForegroundColours.CLEAR_WHITE}'


def mockup_text_as_ok_green(text: str) -> str:
    return f'{ForegroundColours.OK_GREEN} {text} {ForegroundColours.CLEAR_WHITE}'


def mockup_text_as_ok_blue(text: str) -> str:
    return f'{ForegroundColours.OK_BLUE} {text} {ForegroundColours.CLEAR_WHITE}'


def mockup_text_as_header_purple(text: str) -> str:
    return f'{ForegroundColours.HEADER} {text} {ForegroundColours.CLEAR_WHITE}'


def mockup_text_as_fail_red(text: str) -> str:
    return f'{ForegroundColours.FAIL} {text} {ForegroundColours.CLEAR_WHITE}'


def mockup_text_as_bold_white(text: str) -> str:
    return f'{ForegroundColours.BOLD} {text} {ForegroundColours.CLEAR_WHITE}'


def mockup_text_as_clear_white(text: str) -> str:
    return f'{ForegroundColours.CLEAR_WHITE} {text} {ForegroundColours.CLEAR_WHITE}'


def mockup_text_as_underlined_white(text: str) -> str:
    return f'{ForegroundColours.UNDER_LINE} {text} {ForegroundColours.CLEAR_WHITE}'


if __name__ == '__main__':
    print(mockup_text_as_header_purple("Headline News"))  # purple
    print(mockup_text_as_ok_blue("it's ok to be Blue"))  # light blue
    print(mockup_text_as_ok_green("it's also cool to be green"))  # lime
    print(mockup_text_as_warning_yellow("i'm not sure i'm suppose to be doing this?"))  # yellow
    print(mockup_text_as_fail_red("sorry, we don't do this!"))  # red
    print(mockup_text_as_clear_white("hey, how are you..."))  # white
    print(mockup_text_as_bold_white("let's do this!"))  # bold white
    print(mockup_text_as_underlined_white("it's all in the details"))  # under lined text
