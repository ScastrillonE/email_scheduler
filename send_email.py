import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

class Email:

    def __init__(self,**kwargs):
        self.smtp_server = kwargs['smtp_server']
        self.sender_email = kwargs['sender_email']
        self.port = kwargs['port'] if kwargs['port'] else 465
        self.receiver_email = kwargs['receiver_email']
        self.password = kwargs['password']
        self.message_template = Template(kwargs['message_template'])
        self.subject = kwargs['subject']

    def get_contacts(self):
        names = []
        emails = []
        for contact in self.receiver_email:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
        return names, emails

    def send_email(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            names, emails = self.get_contacts()
            for name, email in zip(names,emails):
                #Create message
                msg = MIMEMultipart() 
                #Substitute fields for email
                message = self.message_template.substitute(CLIENT_NAME=name)

                msg['From']=self.sender_email
                msg['To']=email
                msg['Subject']=f"{self.subject}"

                part1 = MIMEText(message, 'plain') #To do: format html to plain text
                part2 = MIMEText(message, 'html')

                msg.attach(part1)
                msg.attach(part2)

                server.send_message(msg)
                