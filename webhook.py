import requests
import json

class Notification:
    def __init__(self,webhook_url,uuid):
        self.webhook_url = webhook_url
        self.uuid = uuid

    def send_notification(self):
        data = {'title':self.title}
        resp = requests.post(self.webhook_url, data=json.dumps(
            data, sort_keys=True, default=str), headers={'Content-Type': 'application/json'}, timeout=1.0)
