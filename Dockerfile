FROM python:3
MAINTAINER Oksana&Yevhen
RUN apt-get update
WORKDIR /opt/config-manager
COPY final.py .
COPY requirements.txt . 
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt && \
 apk --purge del .build-deps
#RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "final.py"]
