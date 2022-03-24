# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.9.10

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/bookapi
COPY requirements.txt ./docker/start-server.sh /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY bookapi /opt/app/bookapi/

EXPOSE 8000
CMD ["/opt/app/start-server.sh"]