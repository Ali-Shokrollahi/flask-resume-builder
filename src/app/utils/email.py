from flask_mail import Message

from flask import current_app

from app.extensions import mail

app = current_app


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)
