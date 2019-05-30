FROM python:3.7.3

WORKDIR /wd

ADD ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ADD ./api/ api
ADD ./resources resources

ENV env dev
ENV DB_HOST postgres
ENV DB_PORT 5432
ENV DB_USER "jelly"
ENV DB_PASSWORD "j3llynote"
ENV DB_NAME jellynote
ENV SERVER_HOST 127.0.0.1
ENV SERVER_PORT 8000
ENV RUN_MIGRATIONS "false"

ADD ./docker/startup.sh startup.sh

CMD /bin/bash startup.sh


