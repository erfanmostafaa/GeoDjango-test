FROM registry.sedrehgroup.ir/python:3.11.1

RUN apt update && apt install -y \
    gdal-bin libgdal-dev libgeos-dev libproj-dev \
    postgresql-client

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

COPY . /app

ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]
