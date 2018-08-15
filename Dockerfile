FROM python:3.6
MAINTAINER jtmihalic@gmail.com

WORKDIR /tmp

RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN apt-get update && \
    apt-get install -y google-chrome-stable unzip && \
    curl -LO https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/

ADD requirements.txt /tmp/
RUN pip install -r requirements.txt

RUN mkdir -p /tmp/screenshot
WORKDIR /tmp/screenshot
ADD screenshot.py /tmp/

#Add start script
ADD start.sh /tmp/
RUN chmod +x /tmp/start.sh

ENTRYPOINT ["/tmp/start.sh"]
