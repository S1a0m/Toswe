# messenger.py — Intégration Nehanda × Facebook Messenger
#
# Démarrage :
#   uvicorn messenger:app --host 0.0.0.0 --port 8002
#
# Sessions persistantes via SQLite (même DB que Nehanda)

import os
import json
import logging
import httpx

from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("messenger")

# ── Config ────────────────────────────────────────────────────
VERIFY_TOKEN    = os.getenv("MESSENGER_VERIFY_TOKEN", "Nehanda_Secret_2026")
PAGE_TOKEN      = os.getenv("MESSENGER_PAGE_TOKEN", "").strip().split('#')[0].strip()
NEHANDA_API_URL = os.getenv("NEHANDA_API_URL", "http://127.0.0.1:8001")

# Même base SQLite que Nehanda — une seule source de vérité
CONV_DB_URL = os.getenv("CONVERSATIONS_DB_URL", "sqlite:///./conversations.db")

if not PAGE_TOKEN:
    logger.warning("MESSENGER_PAGE_TOKEN manquant — les envois échoueront.")

# ═════════════════════════════════════════════════════════════
# Base de données — table messenger_sessions
# ═════════════════════════════════════════════════════════════

engine       = create_engine(
    CONV_DB_URL,
    future=True,
    connect_args={"check_same_thread": False}
    if CONV_DB_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base         = declarative_base()


class MessengerSession(Base):
    """
    Associe un sender_id Messenger à un conversation_id Nehanda.
    Persiste entre les redémarrages du serveur.
    """
    __tablename__ = "messenger_sessions"

    sender_id       = Column(String(64), primary_key=True, index=True)
    conversation_id = Column(Integer, nullable=False)
    updated_at      = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


Base.metadata.create_all(bind=engine)
logger.info("Table messenger_sessions prête.")


# ── Helpers session ───────────────────────────────────────────

def get_conv_id(sender_id: str) -> int | None:
    """Récupère le conversation_id depuis la DB."""
    with SessionLocal() as db:
        row = db.get(MessengerSession, sender_id)
        return row.conversation_id if row else None


def save_conv_id(sender_id: str, conversation_id: int) -> None:
    """Sauvegarde ou met à jour la session en DB."""
    with SessionLocal() as db:
        row = db.get(MessengerSession, sender_id)
        if row:
            row.conversation_id = conversation_id
            row.updated_at      = datetime.utcnow()
        else:
            db.add(MessengerSession(
                sender_id=sender_id,
                conversation_id=conversation_id,
            ))
        db.commit()


# ═════════════════════════════════════════════════════════════
# Helpers Messenger Graph API
# ═════════════════════════════════════════════════════════════

GRAPH_URL = "https://graph.facebook.com/v19.0/me/messages"


async def _send_raw(payload: dict) -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            GRAPH_URL,
            params={"access_token": PAGE_TOKEN},
            json=payload,
        )
        if r.status_code != 200:
            logger.error("Messenger API error %s: %s", r.status_code, r.text)


async def send_text(recipient_id: str, text: str) -> None:
    chunks = [text[i:i+1800] for i in range(0, len(text), 1800)]
    for chunk in chunks:
        await _send_raw({
            "recipient": {"id": recipient_id},
            "message":   {"text": chunk},
        })


async def send_typing(recipient_id: str) -> None:
    await _send_raw({
        "recipient":     {"id": recipient_id},
        "sender_action": "typing_on",
    })


async def send_carousel(recipient_id: str, products: list[dict]) -> None:
    if not products:
        return

    elements = []
    for p in products[:10]:
        if p.get("has_promo") and p.get("promo_price"):
            price_str = f"{int(p['promo_price'])} CFA (promo -{p.get('promo_percent', '')}%)"
        else:
            price_str = f"{p.get('price', 0)} CFA"

        subtitle_parts = [price_str]
        if p.get("rating_avg") and p.get("rating_count", 0) >= 3:
            subtitle_parts.append(f"⭐ {p['rating_avg']}/5 ({p['rating_count']} avis)")
        if p.get("shop_name"):
            subtitle_parts.append(f"📍 {p['shop_name']}")
        if not p.get("in_stock", True):
            subtitle_parts.append("❌ Épuisé")

        if p.get("promo_ends_at"):
            try:
                ends  = datetime.strptime(p["promo_ends_at"], "%Y-%m-%d")
                delta = (ends - datetime.now()).days
                if delta == 0:
                    subtitle_parts.append("⏰ Promo expire aujourd'hui !")
                elif delta == 1:
                    subtitle_parts.append("⏰ Promo expire demain !")
                elif delta <= 3:
                    subtitle_parts.append(f"⏰ Promo encore {delta} jours")
            except ValueError:
                pass

        subtitle    = " · ".join(subtitle_parts)[:80]
        product_url = f"https://toswe-africa.com/product/{p['id']}"

        card: dict = {
            "title":    p.get("name", "Produit")[:80],
            "subtitle": subtitle,
            "buttons": [{
                "type":  "web_url",
                "url":   product_url,
                "title": "🛒 Voir sur Tôswè",
            }],
        }
        if p.get("image_url"):
            card["image_url"] = p["image_url"]

        elements.append(card)

    await _send_raw({
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements":       elements,
                },
            }
        },
    })


async def send_quick_replies(recipient_id: str, text: str,
                             replies: list[str]) -> None:
    await _send_raw({
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
            "quick_replies": [
                {"content_type": "text", "title": r[:20], "payload": r}
                for r in replies[:13]
            ],
        },
    })


# ═════════════════════════════════════════════════════════════
# Appel à l'API Nehanda
# ═════════════════════════════════════════════════════════════

async def call_nehanda(sender_id: str, message: str) -> tuple[str, list[dict]]:
    """
    Appelle Nehanda avec la session persistante du sender.
    Si la session n'existe pas en DB → Nehanda crée une nouvelle conversation
    et on sauvegarde l'ID retourné.
    """
    conv_id = get_conv_id(sender_id)   # ← lecture en DB, pas en RAM

    payload: dict = {"message": message}
    if conv_id:
        payload["conversation_id"] = conv_id

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{NEHANDA_API_URL}/nehanda/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            r.raise_for_status()
            data = r.json()

        new_conv_id = data.get("conversation_id")
        if new_conv_id:
            save_conv_id(sender_id, new_conv_id)   # ← écriture en DB

        return (
            data.get("response", "Désolé, je n'ai pas pu répondre."),
            data.get("products", []),
        )

    except httpx.TimeoutException:
        return "Nehanda est un peu lente là 😔 — réessaie dans quelques secondes !", []
    except Exception as exc:
        logger.error("Erreur appel Nehanda: %s", exc)
        return "Une erreur s'est produite. Réessaie ou contacte le support Tôswè.", []


# ═════════════════════════════════════════════════════════════
# Traitement des événements
# ═════════════════════════════════════════════════════════════

async def handle_message(sender_id: str, message_data: dict) -> None:
    text = message_data.get("text", "").strip()
    if not text:
        await send_text(
            sender_id,
            "Je ne peux traiter que les messages texte pour l'instant 😊 "
            "Dis-moi ce que tu cherches !"
        )
        return

    logger.info("Message de %s : %s", sender_id, text[:50])
    await send_typing(sender_id)

    reply, products = await call_nehanda(sender_id, text)
    await send_text(sender_id, reply)

    if products:
        await send_carousel(sender_id, products)
    elif len(text) < 30:
        await send_quick_replies(
            sender_id,
            "Voici ce que je peux faire pour toi 👇",
            [
                "🔍 Rechercher un produit",
                "🌟 Meilleures notes",
                "📦 Suivre ma commande",
                "ℹ️ C'est quoi Tôswè ?",
            ],
        )


async def handle_postback(sender_id: str, postback: dict) -> None:
    payload = postback.get("payload", "")
    title   = postback.get("title", "")
    logger.info("Postback de %s : %s", sender_id, payload)
    await send_typing(sender_id)
    reply, products = await call_nehanda(sender_id, title or payload)
    await send_text(sender_id, reply)
    if products:
        await send_carousel(sender_id, products)


# ═════════════════════════════════════════════════════════════
# Endpoints FastAPI
# ═════════════════════════════════════════════════════════════

app = FastAPI(title="Nehanda Messenger Bot", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/webhook")
async def verify_webhook(request: Request):
    mode      = request.query_params.get("hub.mode") or request.query_params.get("hub_mode")
    token     = request.query_params.get("hub.verify_token") or request.query_params.get("hub_verify_token")
    challenge = request.query_params.get("hub.challenge") or request.query_params.get("hub_challenge")

    logger.info("Vérification webhook — mode: %s, token: %s", mode, token)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook vérifié ✅")
        return PlainTextResponse(content=str(challenge))

    logger.warning("Échec vérification — reçu: %s | attendu: %s", token, VERIFY_TOKEN)
    return PlainTextResponse(content="Token invalide", status_code=403)


@app.post("/webhook")
async def receive_webhook(request: Request) -> dict:
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON invalide")

    if body.get("object") != "page":
        return {"status": "ignored"}

    for entry in body.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event.get("sender", {}).get("id")
            if not sender_id:
                continue

            if "message" in event and not event["message"].get("is_echo"):
                await handle_message(sender_id, event["message"])
            elif "postback" in event:
                await handle_postback(sender_id, event["postback"])

    return {"status": "ok"}


@app.get("/health")
async def health() -> dict:
    # Vérifie que la DB est accessible
    try:
        with SessionLocal() as db:
            count = db.query(MessengerSession).count()
        db_status = f"ok ({count} sessions)"
    except Exception as e:
        db_status = f"erreur: {e}"

    return {
        "status":      "ok",
        "service":     "Nehanda Messenger Bot v1.1",
        "nehanda_url": NEHANDA_API_URL,
        "db":          db_status,
    }