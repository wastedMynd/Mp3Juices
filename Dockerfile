# Mp3Juices Docker Image
# Creation Date: 25 October 2020, 22:15
# Author: Sizwe-se-Afrika Immaculate Mkhonza

FROM alpine:latest

# setup app dir and copy code base on it...
ENV app_dir=Mp3Juices_Downloader
RUN mkdir -p $app_dir
WORKDIR $app_dir
COPY . .

# import code base dependencies
RUN apk add --update wget && wget https://chromedriver.storage.googleapis.com/83.0.4103.14/chromedriver_linux64.zip
RUN apk add --update unzip && unzip chromedriver_linux64.zip && rm chromedriver_linux64.zip && ls -a
RUN apk add --update chromium && ln -s /usr/bin/chromium-browser /usr/bin/google-chrome
RUN apk add --update python3 && apk add --update py-pip && apk add --update nano
RUN pip install -r requirements.txt

# setup volume for usr/Downloads/mp3juices
ENV selenium_driver=$app_dir/chromedriver
ENV users_downloads_folder=/home/sizwe/Downloads/mp3juices
ENV docker_container_downloads_folder=/usr/Downlaods/mp3juices
ENV mp3juices_download_path=$docker_container_downloads_folder
RUN mkdir -p $docker_container_downloads_folder
VOLUME $users_downloads_folder:$docker_container_downloads_folder

# app's entry point
ENTRYPOINT ["/bin/sh", "-c" ]

CMD ["python3", "-m", "unittest", "test.TestApp"]
CMD ["python3","playlist_download.py"]
CMD ["python3","app.py"]
