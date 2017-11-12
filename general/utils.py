import sendgrid
from django.conf import settings
from sendgrid.helpers.mail import *

def send_email(from_email, subject, to_email, content):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_KEY)

    from_email = Email(from_email, "Globalboard")
    to_email = Email(to_email)

    content = Content("text/html", content)
    mail = Mail(from_email, subject, to_email, content)
    return sg.client.mail.send.post(request_body=mail.get())
