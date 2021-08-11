FROM python:3.8-alpine

RUN adduser -D scheduler

WORKDIR /home/scheduler

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY api.py ./
COPY send_email.py ./

RUN chown -R scheduler:scheduler ./
USER scheduler

CMD ["uvicorn", "api:app", "--reload", "--host", "0.0.0.0", "--port", "5057"]
