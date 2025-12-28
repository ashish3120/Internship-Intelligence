import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_email(content):
    sender_email = "singhsajal177@gmail.com"
    receiver_email = "ashishsingh66652@gmail.com"
    app_password = "xyblllkxmtcuugkt"

    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "Daily Internship Intelligence Report"
    msg["From"] = formataddr(("Internship Intelligence Bot", sender_email))
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()
        print("Email sent successfully")

    except smtplib.SMTPException as e:
        print("Email sending failed:", e)
