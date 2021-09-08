import smtplib
import ssl
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from bs4 import BeautifulSoup



class Email:

    def __init__(self, **kwargs):
        self.smtp_server = kwargs['smtp_server']
        self.sender_email = kwargs['sender_email']
        self.port = kwargs['port'] if kwargs['port'] else 465
        self.receiver_email = kwargs['receiver_email']
        self.password = kwargs['password']
        self.message_template = Template(base64.b64decode(kwargs['message_template']).decode('utf-8'))
        self.subject = kwargs['subject']

    def get_contacts(self):
        names = []
        emails = []
        for contact in self.receiver_email:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
        return names, emails

    def convert_html_text(self,message):


        html = BeautifulSoup(str(message))
        text = html.get_text()
        return text


    def send_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            names, emails = self.get_contacts()
            for name, email in zip(names, emails):
                # Create message
                msg = MIMEMultipart()
                # Substitute fields for email
                message = self.message_template.substitute(CLIENT_NAME=name)

                msg['From'] = self.sender_email
                msg['To'] = email
                msg['Subject'] = f"{self.subject}"

                # To do: format html to plain text
                part1 = MIMEText(self.convert_html_text(message), 'plain')
                print(part1)
                part2 = MIMEText(message, 'html')

                #msg.attach(part1)
                msg.attach(part2)

                server.send_message(msg)
