FROM python:3

RUN echo 'deb http://httpredir.debian.org/debian jessie-backports main' | tee -a /etc/apt/sources.list.d/jessie-backports.list
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
      espeak \
      libespeak-dev \
      ffmpeg

ADD . /app
WORKDIR /app
RUN pip install numpy
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python app.py
