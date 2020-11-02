import os
import threading

from main import open_mp3_juices
from downloader import download_dir
from utils import sleep


def query_file_entry_point() -> None:
    known_open_mp3_juices_responses = [
        {"is_app_running": True, "response": "search query is not provided!"},  # 0
        {"is_app_running": False, "response": "Internet connection is down!"},  # 1
        {"is_app_running": True, "response": "query {} can't be found!"},  # 2
        {"is_app_running": True, "response": "done executing, query {} operation."},  # 3
    ]

    query_file = os.path.join(download_dir, "query.txt")

    os.makedirs(download_dir, exist_ok=True)

    hint = """
        # to skip a query prefix '#'
        # a query example looks like this... 'boys to men'
        #
        # optional function to suffix':' followed by,
        #
        # song selection
        # single selection          1
        # range selection           1-5
        # specific selection        1,3,9, or 'all'
        #
        # actions supported
        # to download type          d
        # to play type              p  
        #
        # working examples:(spaces indentation is optional)
        # boys to men
        # boys to men   :   1-5     :    d 
        # boys to men   :   1,12    :    d
        # boys to men   :   6       :    d
        # boys to men   :   all     :    d
        #
        # note if your query is just like the following...
        # boys to men
        # then the all:d will be suffixed.
        # 
        # your queries...
        # 
        """.strip().replace('\t#', '#')

    if not os.path.exists(query_file):
        with open(query_file, "w") as query_file_creator:
            query_file_creator.write(hint + "\n\n")

    retain_queries = []
    background_tasks = []

    with open(query_file, "r") as query_file_reader:
        for line in query_file_reader.readlines():
            if line.strip() == "" or line.strip() == "\n":
                break

            if line.strip().startswith("#"):  # comment line
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
                    option_param=option if option != '' else "d",
                    quite_mode=True
                )

                if request.get("response") != known_open_mp3_juices_responses[3].get("response").format(with_query):
                    retain_queries.append(with_query)

            background_task = threading.Thread(target=run_app, args=(line.strip(),))
            background_tasks.append(background_task)

    for background_task in background_tasks:
        background_task.start()
        sleep(20)

    for background_task in background_tasks:
        background_task.join()
        sleep(20)

    if not len(retain_queries):
        return None

    queries = hint
    for query in retain_queries:
        queries += "\n# " + query

    with open(query_file, "w") as query_file_writer:
        query_file_writer.write(queries.strip())


if __name__ == '__main__':
    query_file_entry_point()
