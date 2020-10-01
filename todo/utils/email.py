from flask_mail import Message
from flask import current_app
from todo import celery, mail


@celery.task(bind=True, ignore_result=True, default_retry_dalay=300, max_retries=5)
def send_email(self, to, subject, template):
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
    try:
        mail.send(msg)
    except Exception as e:
        self.retry(exc=e)
