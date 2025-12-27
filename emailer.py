import smtplib
from email.mime.text import MIMEText

def send_email(content):
    sender = "singhsajal177@gmail.com"
    password = "chahalGw18@"
    receiver = "ashishsingh66652@gmail.com"

    msg = MIMEText(content)
    msg["Subject"] = "Daily Internship Intelligence"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
