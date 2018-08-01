FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 && chmod +x /usr/local/bin/dumb-init
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir code
WORKDIR /app/code
RUN wget https://raw.githubusercontent.com/MTG/freesound-python/master/freesound.py
ADD ./code/ /app/code/