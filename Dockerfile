FROM apache/spark:3.4.1-scala2.12-java11-python3-ubuntu

WORKDIR /app

USER root

ENV PYTHONPATH="${PYTHONPATH}:/app"

ADD requirements.txt /app
ADD configs /app/configs
ADD scripts /app/scripts
ADD src /app/src

RUN ln -sf $(which python3) /usr/bin/python && \
    ln -sf $(which pip3) /usr/bin/pip

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
