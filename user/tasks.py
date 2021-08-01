from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from vj.settings import ACTIVATE_CODE_AGE


@shared_task(name='send_activated_email')
def send_activated_email(to_email, activate_code):
    subject = f'[VJ]验证码：[{activate_code}]，确认邮件地址'
    text_content = f"""
您的邮箱验证码是：{activate_code}
验证码有效期：{ACTIVATE_CODE_AGE // 60}分钟
"""
    html_content = f"""
<div>
<p>您的邮箱验证码是：<code>{activate_code}</code></p>
<p>验证码有效期：{ACTIVATE_CODE_AGE // 60}分钟</p>
</div>
"""
    email_msg = EmailMultiAlternatives(subject=subject, body=text_content, to=[to_email])
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
