import cli_colour_utils as makeup
from threading import Thread
import os
import random
import requests
import subprocess

env_path = os.environ.get("MP3JUICES_DOWNLOAD_PATH")
base_path = os.path.join(os.environ.get("HOME"), "Downloads/mp3juices")
download_dir = base_path if env_path is None else env_path

characters_to_replace_on_file_name = (
    '#', '<', '$', '+', '%', '>', '!',
    '`', '&', '*', "'", '|', '{', '?',
    '"', '=', '}', '/', ':', '\\', '@',
    ' ', "."
)


def initialize_download(option_type, results, entry_selected, mp3_results_holder, query=None):
    if not (option_type == 'download'):
        print(makeup.mockup_text_as_warning_yellow("selected option type, not download!"))
        return None
    download_element = results.find_element_by_id(f'download_{entry_selected + 1}')
    options = download_element.find_element_by_class_name('options')
    download_url = options.find_element_by_class_name('url').get_attribute('href')

    filename = mp3_results_holder[entry_selected].get("title")
    Thread(target=start_download, args=(filename, download_url, query)).start()


def start_download(filename, download_url, query=None):
    if download_url is None or filename is None:
        print(makeup.mockup_text_as_warning_yellow('file not downloaded, url and filename not provided!'))
        return False

    placeholder_download_dir = os.path.join(download_dir,
                                            resolve_file_name(query)) if query is not None else download_dir

    os.makedirs(placeholder_download_dir, exist_ok=True)
    downloaded_file_path = os.path.join(placeholder_download_dir, resolve_file_name(filename) + ".mp3")

    print(makeup.mockup_text_as_bold_white(f"downloading {filename} started..."), end='\n\r')

    user_agent_list = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/57.0.2987.110 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.79 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
         'Gecko/20100101 '
         'Firefox/55.0'),  # firefox
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.91 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/62.0.3202.89 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/63.0.3239.108 '
         'Safari/537.36'),  # chrome
    ]

    file_size = 0 if not os.path.exists(downloaded_file_path) else os.stat(downloaded_file_path).st_size

    headers = {
        "User-Agent": random.choice(user_agent_list),
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Range': f'bytes={file_size}-'
    }

    try:
        with requests.get(download_url, headers=headers, stream=True) as mp3_file_to_download:
            assert mp3_file_to_download.ok
            with open(downloaded_file_path, 'a+b') as downloaded_file:
                for chunk in mp3_file_to_download.iter_content(chunk_size=1024):
                    downloaded_file.write(chunk)
    except Exception as error:
        print(makeup.mockup_text_as_fail_red(error))
    finally:
        if not os.path.exists(downloaded_file_path):
            print(makeup.mockup_text_as_fail_red(f'{filename} not downloaded, something wrong happened!'), end='\n\r')
            return False
        else:
            change_download_file_permissions(placeholder_download_dir, downloaded_file_path)
            print(
                makeup.mockup_text_as_ok_green(f'{filename} downloaded at, {downloaded_file_path}; download finished.'),
                end='\n\r'
            )
            return True


def resolve_file_name(title: str):
    filename = title.strip()

    for char in characters_to_replace_on_file_name:
        filename = filename.replace(char, "_")

    return filename.strip()


def change_download_file_permissions(folder, file):
    entries = [folder + '/', file]
    modes = ['u', 'g', 'a']
    user = os.environ.get("USER")
    for entry in entries:
        subprocess.run(['chown', "-R", user, entry])
        for mode in modes:
            subprocess.run(['chmod', f'{mode}=rwx', entry])
