import smtplib
from email.message import EmailMessage

class ManagementEmail:
    def __init__(self) -> None:
        self.address = ""
        self.password = ""
        self.file_attachment = ""
        self.message = EmailMessage()
        self.smtp = None

    def authentication_files(self, address_file, password_file):
        with open(address_file) as file:
            self.address = file.read().strip()

        with open(password_file) as file:
            self.password = file.read().strip()

    def headers_email(self, title_email, recipient):
        self.message["Subject"] = title_email
        self.message["From"] = self.address
        self.message["To"] = recipient

    def message_email(self, message):
        self.message.set_content(message)
        
    def email_attachment(self, path_file, attachment_name):
        with open (path_file, "rb") as attachment:
            self.file_attachment = attachment.read()
            self.message.add_attachment(self.file_attachment, maintype="application", subtype="octet-stream", filename=attachment_name)

    def send_message(self):

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.address, self.password)
                smtp.send_message(self.message)
                print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
            
    def close_connection(self):
        if self.smtp:
            self.smtp.quit()
            print("SMTP connection closed.")


# Example Usage
# email_manager = ManagementEmail()
# email_manager.authentication_files(address_file="address.txt", password_file="password.txt")
# email_manager.headers_email(title_email="Send email with Python", recipient="you_email@example.com")
# email_manager.message_email(message="Hello there!")
# email_manager.send_message()
# email_manager.close_connection()
