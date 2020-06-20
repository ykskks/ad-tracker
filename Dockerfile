FROM python:3

RUN apt-get update && apt-get install -y unzip

# google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# chrome driver
RUN mkdir --mode=755 -p /opt/chrome
ADD https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip /opt/chrome
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

COPY requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt
