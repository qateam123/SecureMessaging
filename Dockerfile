FROM ubuntu:14.04

ENV RUNTIME_PACKAGES="python3"
ENV BUILD_PACKAGES="build-essential python3-dev python3-pip"

WORKDIR /code

EXPOSE 5000

RUN apt-get update && apt-get install -y $RUNTIME_PACKAGES $BUILD_PACKAGES

ADD requirements.txt /code/requirements.txt

RUN pip3 install -U -I -r /code/requirements.txt

ADD . /code

ENTRYPOINT ["python3"]
CMD ["run.py"]
