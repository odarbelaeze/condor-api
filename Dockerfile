FROM python:3.6


RUN apt-get update -y -q
RUN apt-get install -y -q enchant aspell-es aspell-en aspell-fr aspell-it aspell-pt aspell-de

ADD ./requirements.txt /
RUN pip install -r requirements.txt
RUN python -m nltk.downloader snowball_data
RUN python -m nltk.downloader stopwords

WORKDIR /app
