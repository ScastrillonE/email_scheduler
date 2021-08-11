from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List, Text
from rq import Queue, queue
from rq.command import send_stop_job_command
from redis import Redis
from datetime import timedelta,datetime
from send_email import Email

redis_connection = Redis(host='myproj_redis')
queue = Queue(connection=redis_connection)

app = FastAPI()

class DataSendEmail(BaseModel):
    smtp_server: str
    sender_email: EmailStr
    port: int
    receiver_email: list
    password: str
    message_template: Text
    subject: str

    

@app.post("/send_email", status_code=201)
def add_task(email: DataSendEmail):
    try:
        instance = Email(**dict(email))
        job = queue.enqueue_in(timedelta(seconds=60),instance.send_email)
        return {"message": 'Added job',"job_id":job.id}
    except Exception as e:
        return {"Error": str(e)}

@app.post("/delete", status_code=201)
def delete_task(job_id:str):
    try:
        send_stop_job_command(redis_connection,job_id)
        return {"Success": f"Job with id {job_id} deleted"}
    except Exception as e:
        return {"Error": str(e)}
