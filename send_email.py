import sys

sys.path.append("youra/path/here")
from ClassSendEmail.management_email import *
import json

with open("content_email.json", "r") as file:
    data = json.load(file)

for information in data:
    email_management = ManagementEmail()

    email_management.authentication_files(
        address_file="address.txt", password_file="password.txt"
    )

    email_management.headers_email(title_email=information["subject"], recipient=information["destiny"])
    email_management.message_email(message=information["content"])
    email_management.email_attachment(path_file="", attachment_name="")
    email_management.send_message()

email_management.close_connection()
