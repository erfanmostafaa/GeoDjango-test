FROM registry.sedrehgroup.ir/python:3.11.1

RUN mkdir /app
WORKDIR /app

COPY requirments.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirments.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
