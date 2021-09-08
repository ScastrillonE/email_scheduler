from datetime import  datetime, timedelta
from typing import List, Text

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from redis.client import Pipeline
from rq import Queue, queue
from rq.job import Job
from rq import cancel_job
from rq.command import send_stop_job_command

from redis import Redis
from send_email import Email
from utils import divide_list_email


redis_connection = Redis(host='myproj_redis')
queue = Queue(connection=redis_connection)

app = FastAPI()

class DataSendEmail(BaseModel):
    smtp_server: str
    sender_email: str
    port: int
    receiver_email: list
    password: str
    message_template: str
    subject: str

class ScheduledDay(BaseModel):
    scheduled_day: str

    

@app.post("/send_email", status_code=201)
def add_task(email: DataSendEmail):
    print("EXECUTE")
    try:
        instance = Email(**dict(email))
        job = queue.enqueue_in(timedelta(seconds=60),instance.send_email)
        return {"success": 'Added job',"job_id":job.id}
    except Exception as e:
        return {"Error": str(e)}

@app.post("/send_email_scheduler", status_code=201)
def add_task__scheduler(email: DataSendEmail,scheduled_day: ScheduledDay):
    scheduled_day  = dict(scheduled_day)['scheduled_day']
    scheduled_day  = datetime.strptime(scheduled_day, '%d/%m/%YT%H:%M')
    try:
        instance = Email(**dict(email))
        job = queue.enqueue_at(scheduled_day,instance.send_email)
        return {"success": 'Added job',"job_id":job.id}
    except Exception as e:
        return {"Error": str(e)}

@app.post("/send_massive_email", status_code=201)
def add_task_massive(email: DataSendEmail):
    divide_list = divide_list_email(email.receiver_email)
    list_job_id = []
    for contact in divide_list:
        email.receiver_email = contact
        instance = Email(**dict(email))
        job = queue.enqueue_in(timedelta(seconds=60),instance.send_email)
        list_job_id.append(job.id)
    return {"success": 'Added job',"job_id":list_job_id}

@app.post("/delete", status_code=201)
def delete_task(job_id:str):
    try:
        job = Job.fetch(job_id, connection=redis_connection)
        job.delete()
        return {"success":f"Job with id {job_id} deleted successfully"}
    except Exception as e:
        return {"Error": str(e)}