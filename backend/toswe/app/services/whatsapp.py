# app/services/whatsapp.py

from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables d'environnement à partir d’un fichier .env

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(account_sid, auth_token)

def send_whatsapp_code(to_number: str, message: str) -> bool:
    """
    Envoie un message WhatsApp via Twilio.
    
    :param to_number: Numéro du destinataire au format WhatsApp (ex: 'whatsapp:+225XXXXXXXX')
    :param message: Message à envoyer
    :return: True si succès, False sinon
    """
    try:
        client.messages.create(
            from_=f'whatsapp:{twilio_whatsapp_number}',
            body=message,
            to=f'whatsapp:{to_number}'
        )
        return True
    except Exception as e:
        print(f"[WhatsApp ERROR] {e}")
        return False
