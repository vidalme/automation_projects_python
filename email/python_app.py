from email.message import EmailMessage
import ssl
import smtplib

email_sender = 'enviar.linuxemailtuto@gmail.com'
email_password = 'ifdn ikcv xzlk atiz'

email_receiver = 'receber.linuxemailtuto@gmail.com'

subject = 'Dont forget to subscribe'
body = """
Vou conseguir um emprego de devops em 2024
"""
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
    smtp.login(email_sender,email_password)
    smtp.sendmail(email_sender,email_receiver,em.as_string())