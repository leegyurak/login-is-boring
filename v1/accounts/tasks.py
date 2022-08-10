from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

@shared_task
def task_send_sign_up_verify_code_email(serializer_data):
    verify_code = serializer_data['verify_code']
    
    send_mail(
        subject='회원가입 인증 메일입니다.',
        message=f'{verify_code}\n해당 문자를 다른 사람과 공유하지 마십시오.',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[serializer_data['email'], ],
        fail_silently=True
    )
    return None