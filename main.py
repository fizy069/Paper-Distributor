import os
import base64
import csv
import random
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PyPDF2 import PdfReader, PdfWriter

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def encrypt_pdf(input_pdf_path, password):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    for page_num in range(len(reader.pages)):
        writer.add_page(reader.pages[page_num])

    writer.encrypt(password)
    
    encrypted_pdf_path = input_pdf_path.replace('.pdf', '_encrypted.pdf')
    with open(encrypted_pdf_path, 'wb') as encrypted_pdf:
        writer.write(encrypted_pdf)
    
    return encrypted_pdf_path, password

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

def process_pdfs(pdf_folder, csv_file):
    service = authenticate_gmail()
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            pdf_filename = row['filename']
            recipient_email = row['email']
            pdf_path = os.path.join(pdf_folder, pdf_filename)
            
            if os.path.exists(pdf_path):
                password = generate_password()
                encrypted_pdf_path, password = encrypt_pdf(pdf_path, password)
                
                email_body = f"Please find the attached PDF.\n\nPassword: {password}\n\nKeep it secure."
                
                send_email_gmail(service, recipient_email, "Your Secure PDF", email_body, encrypted_pdf_path)
                
                os.remove(encrypted_pdf_path)
            else:
                print(f"{pdf_filename} not found in {pdf_folder}")

# Usage
pdf_folder = 'C:/Users/mahir/Desktop/Dev/Python/sop-project/pdf' 
csv_file = 'data.csv'
process_pdfs(pdf_folder, csv_file)
