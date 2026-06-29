import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

from email_service.mail_sender import send_mail

print("Triggering test email...")
success, msg = send_mail("Testing SENSEX update email sender script connection.")
print(f"Test trigger completed. Success: {success}, Message: {msg}")