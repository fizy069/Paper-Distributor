# Answer Sheet Mailer

Python script to help distribution of scanned answer scripts. 

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Enable Gmail API](#step-1-enable-gmail-api)
  - [Step 2: Install Required Python Libraries](#step-2-install-required-python-libraries)
  - [Step 3: Prepare the Directory and CSV File](#step-3-prepare-the-directory-and-csv-file)
- [Usage](#usage)
- [License](#license)

## Features
- Encrypt PDF files with a strong, randomly generated password.
- Send encrypted PDFs as email attachments using the Gmail API.
- Automatically retrieve email addresses and filenames from a CSV file.

## Prerequisites
- **Google Cloud Project** with Gmail API enabled.
- **Python 3.7+** installed on your machine.
- **Pip** package manager.

## Setup Instructions

### Step 1: Enable Gmail API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Navigate to **APIs & Services > Library**.
4. Search for **Gmail API** and enable it.
5. Go to **APIs & Services > Credentials**.
6. Click **Create Credentials > OAuth client ID**.
7. Configure the consent screen if prompted.
8. For **Application type**, select **Desktop app** and then click **Create**.
9. Download the `credentials.json` file and save it in your project directory.

### Step 2: Install Required Python Libraries
Use the following command to install the necessary libraries:
  ` pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client PyPDF2`


### Step 3: Prepare the Directory and CSV File
1. **PDF Folder**: Place all PDFs to be encrypted and sent in a folder (e.g., `C:/Users/mahir/Desktop/Dev/Python/sop-project/pdf`).
2. **CSV File**: Create a CSV file with the following columns:
   - `filename`: The name of the PDF file (including `.pdf` extension).
   - `email`: The recipient's email address.

## Usage
Run the main Python script to process the PDFs in the specified folder, encrypt them, and send them via email.

