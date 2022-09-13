FROM python:3
LABEL author="BDSE_G2"
WORKDIR /app
COPY ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./app .
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]