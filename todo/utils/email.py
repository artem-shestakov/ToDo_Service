from flask_mail import Message, Mail
from flask import current_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Init Flask-Mail object
mail = Mail()


def send_email(to, subject, template):
    """
    Send email
    :param to: Email recipient
    :param subject: The subject of email
    :param template: Email html template
    """
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


# def send_email(to, subject, template):
#     msg = MIMEMultipart("alternative")
#     msg.attach(MIMEText(template, "html"))
#     msg["Subject"] = subject
#
#     msg["From"] = "ToDo"
#     msg["To"] = to
#
#     smtp_server = smtplib.SMTP(current_app.config['MAIL_SERVER'], 587)
#     smtp_server.starttls()
#     smtp_server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
#     smtp_server.sendmail("", [to], msg.as_string())
#     smtp_server.close()
