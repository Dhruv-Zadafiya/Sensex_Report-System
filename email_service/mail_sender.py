import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import EMAIL, APP_PASSWORD

logger = logging.getLogger(__name__)

def save_report_locally(report_data):
    """
    Saves a local backup of the HTML report if email dispatch fails.
    """
    os.makedirs(os.path.join("reports", "local_copies"), exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"report_{timestamp}.html"
    file_path = os.path.join("reports", "local_copies", file_name)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_data.get("html", report_data.get("text", "")))
        logger.info(f"Local backup copy of the report saved to: {os.path.abspath(file_path)}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to write local backup copy of report: {e}")
        return None

def send_mail(report_data):
    """
    Sends the HTML report via Gmail SMTP server.
    Falls back to writing a local HTML file if SMTP connection or login fails.
    """
    # If report_data is just a string (old code fallback), handle it
    if isinstance(report_data, str):
        report_data = {
            "text": report_data,
            "html": f"<html><body><pre>{report_data}</pre></body></html>",
            "is_gain": True,
            "change_str": "N/A"
        }

    if not EMAIL or not APP_PASSWORD:
        logger.warning("SMTP configuration is missing. Saving local copy instead.")
        local_path = save_report_locally(report_data)
        return False, f"Missing SMTP credentials. Saved locally to {local_path}"

    try:
        logger.info(f"Connecting to SMTP server (smtp.gmail.com:587) to send email to {EMAIL}...")
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"SENSEX Market Update: {report_data.get('change_str', '')}"
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        
        msg.attach(MIMEText(report_data["text"], "plain"))
        msg.attach(MIMEText(report_data["html"], "html"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
        server.quit()
        
        logger.info("Stock market report email sent successfully!")
        return True, "Email sent successfully"
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {e}. Please ensure you are using a 16-character Gmail App Password.")
        local_path = save_report_locally(report_data)
        return False, f"SMTP Auth Failure. Report backup saved locally to: {local_path}"
    except Exception as e:
        logger.error(f"SMTP Dispatch error occurred: {e}")
        local_path = save_report_locally(report_data)
        return False, f"SMTP dispatch error: {e}. Report backup saved locally to: {local_path}"