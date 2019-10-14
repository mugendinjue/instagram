from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name,receiver):
  subject = 'Welcome to Insta clone by denis'
  sender = 'denismugendinjue9@gmail.com'
  text_content = render_to_string('email/welcome.txt',{"name":name})
  html_content = render_to_string('email/welcome.html',{"name":name})
  msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
  msg.attach_alternative(html_content,'text/html')
  msg.send()