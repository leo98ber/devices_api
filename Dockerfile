FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

COPY ./start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

EXPOSE 6740