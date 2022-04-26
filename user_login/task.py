from celery import shared_task
# from time import sleep
from django.core.mail import send_mail
from SC import settings


@shared_task
def send_otp_task(email, user_otp):
    mess = f"Hello {email}, \n Your OTP is {user_otp} \n Thank You"
    send_mail(
        "Welcome",
        mess,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    print("email sent successfully.....!")


# from SC.celery import app 
# from .models import Account
# from datetime import datetime
# from django.core.mail import send_mail
# from django.conf import settings
# print(type(datetime))
# print(datetime.now())
# @app.task(name='send_notification')
# def send_notification():
#     try:
#         time_threshold = datetime.now()
#         account_objs = Account.objects.filter(is_verified=False, created_at__gte = time_threshold)

#         for acc in account_objs:
#             subject = 'Notification: Your account is not verified.'
#             message = 'Still your account is not verified'
#             email_from = settings.EMAIL_HOST_USER
#             recipient = [acc.email]
            
#             send_mail(subject, message, email_from, recipient)
#             print('sent the mail.....successfully')
#     except Exception as e:
#         print(e)