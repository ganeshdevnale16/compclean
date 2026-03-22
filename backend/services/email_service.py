# # import smtplib
# # from email.message import EmailMessage

# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587

# # EMAIL_USER = "deloittecompliancesystem@gmail.com"
# # EMAIL_PASS = "zzfc ttss nvuw qit"


# # def send_email(to, subject, body, attachment=None):

# #     msg = EmailMessage()

# #     msg["Subject"] = subject
# #     msg["From"] = EMAIL_USER
# #     msg["To"] = to

# #     msg.set_content(body)

# #     if attachment:

# #         with open(attachment, "rb") as f:
# #             file_data = f.read()

# #         msg.add_attachment(
# #             file_data,
# #             maintype="application",
# #             subtype="octet-stream",
# #             filename=attachment.split("/")[-1]
# #         )

# #     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

# #         server.starttls()

# #         server.login(EMAIL_USER, EMAIL_PASS)

# #         server.send_message(msg)



# import smtplib
# from email.message import EmailMessage
# import os

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# EMAIL_USER = "deloittecompliancesystem@gmail.com"
# EMAIL_PASS = "xxlr edel dkyl vmsy"


# def send_email(to, subject, body, attachment=None):

#     msg = EmailMessage()

#     msg["Subject"] = subject
#     msg["From"] = EMAIL_USER
#     msg["To"] = to

#     msg.set_content(body)

#     if attachment and os.path.exists(attachment):

#         with open(attachment, "rb") as f:
#             file_data = f.read()

#         msg.add_attachment(
#             file_data,
#             maintype="application",
#             subtype="octet-stream",
#             filename=os.path.basename(attachment)
#         )

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

#         server.starttls()
#         server.login(EMAIL_USER, EMAIL_PASS)

#         server.send_message(msg)







# import smtplib
# from email.message import EmailMessage
# import os

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# EMAIL_USER = "deloittecompliancesystem@gmail.com"
# EMAIL_PASS = "xxlr edel dkyl vmsy"


# def send_email(to, subject, body, attachment=None):

#     msg = EmailMessage()

#     msg["Subject"] = subject
#     msg["From"] = EMAIL_USER
#     msg["To"] = to

#     msg.set_content(body)

#     if attachment and os.path.exists(attachment):

#         with open(attachment, "rb") as f:
#             file_data = f.read()

#         msg.add_attachment(
#             file_data,
#             maintype="application",
#             subtype="octet-stream",
#             filename=os.path.basename(attachment)
#         )

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:










import smtplib
from email.message import EmailMessage
import os

EMAIL_USER = "deloittecompliancesystem@gmail.com"
EMAIL_PASS = "xxlr edel dkyl vmsy"


def send_email(to, subject, body, attachment=None):

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to
    msg.set_content(body)

    if attachment and os.path.exists(attachment):
        with open(attachment, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(attachment)
            )

    try:
        # ✅ SSL instead of TLS
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print("Email sent")

    except Exception as e:
        print("Email error:", str(e))
        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASS)

        server.send_message(msg)
