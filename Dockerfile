FROM python:3.8-slim

ENV AWS_SECRET_ACCESS_KEY=PtYgjmUhBel31iEl2hpChYgCfrL1spNxnyVmihA+
ENV PSE_API_KEY=pse_live_9f8c2a71d4e64b0fa3c1e5d7b2a9c6e1

RUN apt-get update && apt-get install -y gcc curl vim sqlite3

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/src
EXPOSE 8000 22

CMD ["uvicorn", "micita.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
