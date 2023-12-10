#docker build -t alt:python310 .
#docker run -it --gpus all -v `pwd`:/app -p 8888:8888 --name alt alt:python310 bash
#jupyter-lab --ip=0.0.0.0 --no-browser --allow-root

FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y locales locales-all
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN apt update
RUN apt install -y --no-install-recommends python3-pip python3-dev nano wget git
RUN python3 -m pip install --no-cache-dir setuptools
RUN pip install --upgrade pip

RUN pip install openai
RUN pip install jupyterlab

WORKDIR /app
ADD . /app