FROM python:3.8

RUN apt update

EXPOSE 8000

WORKDIR /service/
COPY main.py .
COPY entrypoint.sh .
COPY requirements.txt .
RUN chmod +x ./entrypoint.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]