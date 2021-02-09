import os
import threading

from main import open_mp3_juices
from downloader import download_dir
from utils import sleep


def query_file_entry_point():
    known_open_mp3_juices_responses = [
        {"is_app_running": True, "response": "search query is not provided!"},  # 0
        {"is_app_running": False, "response": "Internet connection is down!"},  # 1
        {"is_app_running": True, "response": "query {} can't be found!"},  # 2
        {"is_app_running": True, "response": "done executing, query {} operation."},  # 3
    ]

    query_file = os.path.join(download_dir, "query.txt")

    os.makedirs(download_dir, exist_ok=True)

    if not os.path.exists(query_file):
        with open(query_file, "x") as query_file_creator:
            print("created query file")

    with open(query_file, "r") as query_file_reader:
        grouping = None
        for line in query_file_reader.readlines():
            if line.strip() == "" or line.strip() == "\n":
                break

            if line.strip().startswith("#"):  # comment line
                if line.find('@'):
                    grouping = line.strip("#@ ").strip()
                elif line.find('##'):
                    grouping = None
                continue

            def run_app(with_query):
                if not (with_query.find(':') > 0):
                    with_query = with_query.strip() + '::'

                meta_data = with_query.strip().split(":")
                selection = meta_data[1]
                option = meta_data[2]

                request = open_mp3_juices(
                    search_query=meta_data[0],
                    selection_param=selection if selection != '' else "all",
                    grouping=grouping,
                    option_param=option if option != '' else "d",
                    quite_mode=True
                )

            threading.Thread(target=run_app, args=(line.strip(),)).start()
            sleep(20)


if __name__ == '__main__':
    query_file_entry_point()
