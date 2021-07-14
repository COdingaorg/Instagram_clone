from pinstagram import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

#sending a welcome email
def send_new_user_email(name, receiver):
  #creating subject and sender
  subject = 'Welcome to Pinstagram'
  sender = settings.EMAIL_HOST_USER

  #context variables
  text_context = render_to_string('email/welcome.txt', {'name':name})
  html_context = render_to_string('email/welcome.html', {'name':name})

  msg = EmailMultiAlternatives(subject, text_context, sender, [receiver])
  msg.attach_alternative(html_context, 'text/html')
  msg.send()