import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_email_gmail(service, recipient_email, subject, body, attachment_path):
    message = MIMEMultipart()
    message['to'] = recipient_email
    message['subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw_message}

    try:
        service.users().messages().send(userId="me", body=message_body).execute()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def extract_email_from_filename(filename):
    base_name = os.path.splitext(filename)[0]  
    year = base_name[:4] 
    roll_number = base_name[8:12] 
    email = f"f{year}{roll_number}@goa.bits-pilani.ac.in"
    # print(f"Extracted email: {email}")
    return email

def process_pdfs(pdf_folder):
    service = authenticate_gmail()
    counter = 1

    for pdf_filename in os.listdir(pdf_folder):
        if pdf_filename.endswith('.pdf'):
            recipient_email = extract_email_from_filename(pdf_filename)
            pdf_path = os.path.join(pdf_folder, pdf_filename)

            if os.path.exists(pdf_path):
                email_body = f"Hello,\n\nPlease find your answer sheet attached."
                send_email_gmail(service, recipient_email, "OS Answer sheet", email_body, pdf_path)
                print(f"Email number {counter} sent to {recipient_email}")
                counter += 1
            else:
                print(f"{pdf_filename} not found in {pdf_folder}")

# Usage
pdf_folder = 'pdf' 
process_pdfs(pdf_folder)
