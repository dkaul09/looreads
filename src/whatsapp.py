from twilio.rest import Client
from src.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
    RECIPIENT_PHONE,
)

_CHUNK_SIZE = 1590  # Twilio WhatsApp hard limit is 1600 chars per message


def send_digest(message: str) -> None:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    chunks = [message[i:i + _CHUNK_SIZE] for i in range(0, len(message), _CHUNK_SIZE)]
    for chunk in chunks:
        client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=RECIPIENT_PHONE,
            body=chunk,
        )
