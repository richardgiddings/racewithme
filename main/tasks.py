from django.core.mail import EmailMessage
from django_rq import job     

@job("email")
def send_email(subject, body, recipient_list):
    msg = EmailMessage(subject=subject, body=body, to=recipient_list)
    msg.send()
