FROM python:3.9.18-slim-bookworm

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./api ./api
EXPOSE 4000

CMD ["flask","--app", "./api/main.py" ,"--debug","run","--host=0.0.0.0", "--port=4000" ]