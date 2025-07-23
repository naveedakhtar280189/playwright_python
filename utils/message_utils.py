import json
import requests
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.mime.application import MIMEApplication
from datetime import datetime
import os
from twilio.rest import Client

def send_slack_message(message):
    config_path = "data/config.json"
    config = read_json_config(config_path)
    webhook_url = config["slack_webhook"]
    try:
        payload = {"text": message}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(webhook_url, json=payload, headers=headers)

        if response.status_code == 200:
            print("[PASS] Slack message sent successfully.")
            return True
        elif response.status_code == 401:
            raise PermissionError("[ERROR] Unauthorized: Check webhook URL or authentication.")
        else:
            raise Exception(f"[ERROR] Failed to send Slack message. Status: {response.status_code}, Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] Network/connection issue: {str(e)}")
    except Exception as e:
        raise Exception(f"[ERROR] Unexpected error sending Slack message: {str(e)}")

def send_teams_message(message):
    config_path = "data/config.json"
    config = read_json_config(config_path)
    webhook_url = config["teams_webhook"]
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": "Automation Notification",
            "themeColor": "0076D7",
            "title": "Test Automation Update",
            "text": message
        }

        response = requests.post(webhook_url, json=payload, headers=headers)

        if response.status_code == 200:
            print("[PASS] Teams message sent successfully.")
            return True
        elif response.status_code == 401:
            raise PermissionError("[ERROR] Unauthorized: Check your Teams webhook URL.")
        else:
            raise Exception(f"[ERROR] Failed to send Teams message. Status: {response.status_code}, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"[ERROR] Network or connection issue: {str(e)}")
    except Exception as e:
        raise Exception(f"[ERROR] Unexpected error sending Teams message: {str(e)}")

def read_json_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def send_email_from_config(
    config_path: str = "data/config.json",
    allure_summary: dict = None,
    overall_status: str = "Pass",
    project_root: str = os.getcwd()
):
    try:
        # Load config
        config = read_json_config(config_path)
        sender_email = config["sender_email"]
        sender_name = config.get("sender_name", "Automation Bot")
        sender_password = config["sender_password"]
        smtp_server = config.get("smtp_server", "smtp.gmail.com")
        smtp_port = config.get("smtp_port", 465)

        to_emails = config.get("to_emails", [])
        cc_emails = config.get("cc_emails", [])
        subject_template = config.get("subject_template", "Automation Report | {date_time} | {status}")
        body_template = config.get("body_template", "Execution completed at {date_time}.\nStatus: {status}")
        attachment_relative_paths = config.get("attachment_relative_paths", [])

        # Create the email
        msg = EmailMessage()
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = ', '.join(to_emails)
        msg['Cc'] = ', '.join(cc_emails)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = allure_summary or {}

        subject = subject_template.format(date_time=now, status=overall_status)
        body = body_template.format(date_time=now, status=overall_status, **summary)

        msg['Subject'] = subject
        msg.set_content(body)

        # Attach files
        for rel_path in attachment_relative_paths:
            abs_path = os.path.join(project_root, rel_path)
            if os.path.exists(abs_path):
                with open(abs_path, 'rb') as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(abs_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(abs_path)}"'
                    msg.attach(part)
            else:
                print(f"[WARN] Attachment not found: {abs_path}")

        # Send the email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("[PASS] Email sent successfully.")
        return True

    except smtplib.SMTPAuthenticationError:
        raise Exception("[ERROR] SMTP authentication failed. Please check your credentials.")
    except FileNotFoundError as fe:
        raise fe
    except Exception as e:
        raise Exception(f"[ERROR] Failed to send email: {str(e)}")

def send_sms_from_config(config_path, to_number, message_body):
    try:
        config = read_json_config(config_path)
        account_sid = config.get("twilio_account_sid")
        auth_token = config.get("twilio_auth_token")
        from_number = config.get("twilio_from_number")

        if not all([account_sid, auth_token, from_number]):
            raise ValueError("[ERROR] Missing Twilio configuration values.")

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )

        print(f"[PASS] SMS sent successfully. SID: {message.sid}")
        return message.sid

    except Exception as e:
        raise Exception(f"[ERROR] Failed to send SMS: {str(e)}")

