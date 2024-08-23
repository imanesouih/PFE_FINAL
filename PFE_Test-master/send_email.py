import os
import glob
import yaml
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import pdfkit

def convert_html_to_pdf(html_path, pdf_path):
    # Path to the wkhtmltopdf executable
    path_to_wkhtmltopdf = os.getenv('WKHTMLTOPDF_PATH', '/usr/local/bin/wkhtmltopdf')  # Valeur par défaut pour Linux

    # Configure pdfkit to use the specified path to wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    # Convert HTML file to PDF
    pdfkit.from_file(html_path, pdf_path, configuration=config)

def send_email(to_address, subject, body, attachment_path):
    from_address = "douah.bilaal98@gmail.com"
    password = "zwsbpghcrrvefbvb"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'html'))

    # Check if the attachment exists and add it
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
        encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(part)
    else:
        print(f"Attachment not found or path is invalid: {attachment_path}")

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_address, password)
            server.sendmail(from_address, to_address, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print("Something went wrong...", e)

def get_to_addresses(env):
    with open(f'environments/{env}.yml', 'r') as file:
        data = yaml.safe_load(file)
    return data['to_addresses']

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python send_email.py [environment]")
        sys.exit(1)

    env = sys.argv[1]
    if env not in ["preprod", "recette"]:
        print("Invalid environment. Must be either 'preprod' or 'recette'")
        sys.exit(1)

    # Define the email parameters
    to_addresses = get_to_addresses(env)
    subject = "PFE Test Results"
    body = "Please find the attached report for the PFE Test."

    # Find the latest HTML file in the results directory
    html_files = glob.glob("results/*.html")
    latest_html_file = max(html_files, key=os.path.getctime)

    # Convert the latest HTML file to PDF
    if latest_html_file:
        pdf_file_path = os.path.splitext(latest_html_file)[0] + ".pdf"
        convert_html_to_pdf(latest_html_file, pdf_file_path)
        attachment_path = pdf_file_path
    else:
        print("No HTML files found in the results directory")
        attachment_path = None

    # Send the email with the PDF attachment
    for to_address in to_addresses:
        send_email(to_address, subject, body, attachment_path)
