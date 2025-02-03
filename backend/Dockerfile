FROM registry.sedrehgroup.ir/python:3.8

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install binutils libproj-dev gdal-bin

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

COPY . /app

COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
