FROM tiangolo/uwsgi-nginx-flask:latest
RUN apt-get update
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
