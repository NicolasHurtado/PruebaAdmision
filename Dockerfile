FROM python:3.8.3-slim
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 5000
CMD ["python", "app.py"]