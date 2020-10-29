# Mp3Juices Docker Image
# Creation Date: 25 October 2020, 22:15
# Author: Sizwe-se-Afrika Immaculate Mkhonza

# set the base image as
FROM ubuntu:latest

# setup app dir and copy code base on it...
ENV APP_DIR=Mp3Juices_Downloader

# create app_dir directory
RUN mkdir -p $APP_DIR

# declare work directory; as $app_dir
WORKDIR $APP_DIR

# copy all app's files, and folders; to work directory.
# note files and folders; metioned on .dockerignore, will be ignored, and not copied
COPY . .

#region setup volume for usr/Downloads/mp3juices

# my                        Downloads/mp3juices folder
ENV USERS_DOWNLOADS_FOLDER=$HOME/Downloads/mp3juices

# this container's          Downloads/mp3juices folder
ENV DOCKER_CONTAINER_DOWNLOADS_FOLDER=/Downloads/mp3juices

# app's                     Downloads/mp3juices folder
# is either mine or containter;
# on container defualts to container's
# on this app defualts to mine's
ENV MP3JUICES_DOWNLOAD_PATH=$DOCKER_CONTAINER_DOWNLOADS_FOLDER

# create container's        Downloads/mp3juices folder
RUN mkdir -p $DOCKER_CONTAINER_DOWNLOADS_FOLDER

# link my Downloads/mp3juices folder to container's Downloads/mp3juices folder
VOLUME $USERS_DOWNLOADS_FOLDER:$DOCKER_CONTAINER_DOWNLOADS_FOLDER

#endregion

#region import code base dependencies
RUN apt update && apt install -y wget && apt install -y unzip && apt install -y nano && apt install -y python3 && apt install -y python3-pip  && pip3 install -r requirements.txt

# region chrome installation workflow along with chromedriver

#  download chrome version 86.0.4240.111-1 on $app_dir
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# install chrome on container
RUN DEBIAN_FRONTEND="noninteractive" apt install -y -f ./google-chrome-stable_current_*.deb

# remove or delete chrome's downloaded installlation file
RUN rm ./google-chrome-stable_current_*.deb

# download chromedriver version 86.0.4240.22 on $app_dir
RUN wget https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip

# unzip downloaded zip file
RUN unzip chromedriver_linux*.zip

# remove or delete downloaded zip file
RUN rm chromedriver_linux*.zip

# diplay list of files/folders on $app_dir
RUN ls -l -a -F -s -h
# endregion
#endregion

# app's entry point
ENTRYPOINT   ["python3","playlist_download.py"]

# after scripting this Dockerfile run this on command on this directory...
# `docker build -t mp3juice:latest .`

# and this command afterwards...
# `docker run -d --name mp3juices_delicious -v $DOWNLOADS_MP3JIUCES:$DOCKER_DOWNLOADS_MP3JUICES mp3juices:latest`

