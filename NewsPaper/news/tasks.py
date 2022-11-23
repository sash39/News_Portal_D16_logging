from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def mail_new():
    post = Post.save(commit=False)
    html_content = render_to_string(
        'news/post_created_email.html',
        {
            'post': post,
            'text': post.preview,
            'link': f'http://127.0.0.1:8000/news/{post.pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{post.title}',
        body=post.text,
        from_email='s1a9s8h6a@yandex.ru',
        to=Category.subscribers
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()


