import smtplib
from email.message import EmailMessage
import streamlit as st

def send_email_with_attachment(to_email, subject, body, attachment_paths):
    email = st.secrets['email']['email']
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = to_email
    msg.set_content(body)

    # Attach files to the email
    for path in attachment_paths:
        try:
            with open(path, "rb") as file:  # Open file in binary mode
                file_data = file.read()  # Read file content
                file_name = file.name  # Get the file name
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
        except:
            continue

    # Sending email through Gmail's SMTP server with SSL on port 465
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email, st.secrets['email']['password'])
        smtp.send_message(msg)
