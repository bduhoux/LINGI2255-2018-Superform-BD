import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException
from flask import current_app
import json

FIELDS_UNAVAILABLE = ['Title','Description'] #list of field names that are not used by your module

CONFIG_FIELDS = ["sender","receiver"] #This lets the manager of your module enter data that are used to communicate with other services.

# appelé dans publishings.py
def run(publishing,channel_config): #publishing:DB channelconfig:DB channel
    json_data = json.loads(channel_config) # to a Python object
    sender = json_data['sender'] # data sur le sender ds channelconfig(= dictionnaire)
    receivers = json_data['receiver'] # data sur le receiver ds channelconfig(= dictionnaire)
    msg = MIMEMultipart() # # Create the container email message
    msg['From'] = sender
    msg['To'] = receivers
    msg['Subject'] = publishing.title

    body = publishing.description
    msg.attach(MIMEText(body, 'plain')) # ajouter contenu texte publication

    try:
        smtpObj = smtplib.SMTP(current_app.config["SMTP_HOST"],current_app.config["SMTP_PORT"])
        if current_app.config["SMTP_STARTTLS"]:
            smtpObj.starttls()
        text = msg.as_string()
        smtpObj.sendmail(sender, receivers, text)
        smtpObj.quit()
    except SMTPException as e:
        #TODO should add log here
        print(e)