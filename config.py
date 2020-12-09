from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_SYNC_SID = os.environ['TWILIO_SYNC_SID']