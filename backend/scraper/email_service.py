# import smtplib
# from email.message import EmailMessage

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# EMAIL_USER = "deloittecompliancesystem@gmail.com"
# EMAIL_PASS = "zzfc ttss nvuw qit"


# def send_email(to, subject, body, attachment=None):

#     msg = EmailMessage()

#     msg["Subject"] = subject
#     msg["From"] = EMAIL_USER
#     msg["To"] = to

#     msg.set_content(body)

#     if attachment:

#         with open(attachment, "rb") as f:
#             file_data = f.read()

#         msg.add_attachment(
#             file_data,
#             maintype="application",
#             subtype="octet-stream",
#             filename=attachment.split("/")[-1]
#         )

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

#         server.starttls()

#         server.login(EMAIL_USER, EMAIL_PASS)

#         server.send_message(msg)



import smtplib
from email.message import EmailMessage
import os

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_USER = "deloittecompliancesystem@gmail.com"
EMAIL_PASS = "zzfc ttss nvuw qit"


def send_email(to, subject, body, attachment=None):

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to

    msg.set_content(body)

    if attachment and os.path.exists(attachment):

        with open(attachment, "rb") as f:
            file_data = f.read()

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=os.path.basename(attachment)
        )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        server.send_message(msg)