# messenger.py — Intégration Nehanda × Facebook Messenger
#
# Démarrage :
#   uvicorn messenger:app --host 0.0.0.0 --port 8002
#
# Ce fichier est indépendant de nehanda_app.py.
# Il reçoit les messages Messenger, appelle l'API Nehanda,
# et renvoie les réponses + carousels produits.

import os
import json
import logging
import httpx

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("messenger")

# ── Config (à mettre dans .env) ───────────────────────────────
# MESSENGER_VERIFY_TOKEN   → token que TU choisis pour vérifier le webhook Meta
# MESSENGER_PAGE_TOKEN     → token de la Page Facebook (depuis Meta for Developers)
# NEHANDA_API_URL          → URL de ton API Nehanda (ex: http://localhost:8001)

VERIFY_TOKEN    = os.getenv("MESSENGER_VERIFY_TOKEN", "nehanda_toswe_secret")
PAGE_TOKEN      = os.getenv("MESSENGER_PAGE_TOKEN", "")
NEHANDA_API_URL = os.getenv("NEHANDA_API_URL", "http://127.0.0.1:8001")

if not PAGE_TOKEN:
    logger.warning("MESSENGER_PAGE_TOKEN manquant — les envois échoueront.")

app = FastAPI(title="Nehanda Messenger Bot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═════════════════════════════════════════════════════════════
# Mémoire des conversations (user_id → conversation_id Nehanda)
# En production : remplace par Redis ou une DB
# ═════════════════════════════════════════════════════════════

_sessions: dict[str, int] = {}

# ═════════════════════════════════════════════════════════════
# Helpers Messenger Graph API
# ═════════════════════════════════════════════════════════════

GRAPH_URL = "https://graph.facebook.com/v19.0/me/messages"


async def _send_raw(payload: dict) -> None:
    """Envoie un payload brut à l'API Messenger."""
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(
            GRAPH_URL,
            params={"access_token": PAGE_TOKEN},
            json=payload,
        )
        if r.status_code != 200:
            logger.error("Messenger API error %s: %s", r.status_code, r.text)


async def send_text(recipient_id: str, text: str) -> None:
    """Envoie un message texte simple."""
    # Messenger limite à 2000 caractères par message
    chunks = [text[i:i+1800] for i in range(0, len(text), 1800)]
    for chunk in chunks:
        await _send_raw({
            "recipient": {"id": recipient_id},
            "message":   {"text": chunk},
        })


async def send_typing(recipient_id: str) -> None:
    """Affiche l'indicateur de frappe."""
    await _send_raw({
        "recipient":     {"id": recipient_id},
        "sender_action": "typing_on",
    })


async def send_carousel(recipient_id: str, products: list[dict]) -> None:
    """
    Envoie un carousel de cartes produits.
    Messenger supporte max 10 éléments par carousel.
    Chaque carte : image + titre + sous-titre + bouton.
    """
    if not products:
        return

    elements = []
    for p in products[:10]:
        # Prix affiché (promo ou normal)
        if p.get("has_promo") and p.get("promo_price"):
            price_str = f"{int(p['promo_price'])} CFA (promo -{p.get('promo_percent', '')}%)"
        else:
            price_str = f"{p.get('price', 0)} CFA"

        # Sous-titre : prix + note + boutique
        subtitle_parts = [price_str]
        if p.get("rating_avg") and p.get("rating_count", 0) >= 3:
            subtitle_parts.append(f"⭐ {p['rating_avg']}/5 ({p['rating_count']} avis)")
        if p.get("shop_name"):
            subtitle_parts.append(f"📍 {p['shop_name']}")
        if not p.get("in_stock", True):
            subtitle_parts.append("❌ Épuisé")

        # Urgence promo
        if p.get("promo_ends_at"):
            from datetime import datetime
            try:
                ends = datetime.strptime(p["promo_ends_at"], "%Y-%m-%d")
                delta = (ends - datetime.now()).days
                if delta == 0:
                    subtitle_parts.append("⏰ Promo expire aujourd'hui !")
                elif delta == 1:
                    subtitle_parts.append("⏰ Promo expire demain !")
                elif delta <= 3:
                    subtitle_parts.append(f"⏰ Promo encore {delta} jours")
            except ValueError:
                pass

        subtitle = " · ".join(subtitle_parts)[:80]  # limite Messenger

        # Bouton → lien vers l'app ou le site
        product_url = f"https://toswe-africa.com/product/{p['id']}"

        card: dict = {
            "title":    p.get("name", "Produit")[:80],
            "subtitle": subtitle,
            "buttons": [
                {
                    "type":  "web_url",
                    "url":   product_url,
                    "title": "🛒 Voir sur Tôswè",
                }
            ],
        }

        # Image si disponible
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
    """Envoie un message avec des boutons de réponse rapide."""
    await _send_raw({
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title":        r[:20],
                    "payload":      r,
                }
                for r in replies[:13]  # limite Messenger : 13 quick replies
            ],
        },
    })


# ═════════════════════════════════════════════════════════════
# Appel à l'API Nehanda
# ═════════════════════════════════════════════════════════════

async def call_nehanda(sender_id: str, message: str) -> tuple[str, list[dict]]:
    """
    Envoie un message à l'API Nehanda et retourne (réponse, produits).
    Maintient la session conversation par sender_id.
    """
    conv_id = _sessions.get(sender_id)

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

        # Sauvegarde de la conversation
        new_conv_id = data.get("conversation_id")
        if new_conv_id:
            _sessions[sender_id] = new_conv_id

        response_text = data.get("response", "Désolé, je n'ai pas pu répondre.")
        products      = data.get("products", [])

        return response_text, products

    except httpx.TimeoutException:
        return "Nehanda est un peu lente là 😔 — réessaie dans quelques secondes !", []
    except Exception as exc:
        logger.error("Erreur appel Nehanda: %s", exc)
        return "Une erreur s'est produite. Réessaie ou contacte le support Tôswè.", []


# ═════════════════════════════════════════════════════════════
# Traitement des événements Messenger
# ═════════════════════════════════════════════════════════════

async def handle_message(sender_id: str, message_data: dict) -> None:
    """Traite un message entrant."""

    # Ignore les messages sans texte (stickers, gifs, etc.)
    text = message_data.get("text", "").strip()
    if not text:
        await send_text(
            sender_id,
            "Je ne peux traiter que les messages texte pour l'instant 😊 "
            "Dis-moi ce que tu cherches !"
        )
        return

    logger.info("Message de %s : %s", sender_id, text[:50])

    # Indicateur de frappe pendant que Nehanda réfléchit
    await send_typing(sender_id)

    # Appel Nehanda
    reply, products = await call_nehanda(sender_id, text)

    # Envoi de la réponse texte
    await send_text(sender_id, reply)

    # Envoi du carousel si des produits sont retournés
    if products:
        await send_carousel(sender_id, products)

    # Quick replies contextuels si pas de produits
    elif not products and len(text) < 30:
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
    """Traite les clics sur les boutons postback."""
    payload = postback.get("payload", "")
    title   = postback.get("title", "")
    logger.info("Postback de %s : %s", sender_id, payload)

    # Traite le postback comme un message texte normal
    await send_typing(sender_id)
    reply, products = await call_nehanda(sender_id, title or payload)
    await send_text(sender_id, reply)
    if products:
        await send_carousel(sender_id, products)


# ═════════════════════════════════════════════════════════════
# Endpoints FastAPI
# ═════════════════════════════════════════════════════════════

@app.get("/webhook")
async def verify_webhook(request: Request) -> Response:
    """
    Vérification du webhook par Meta.
    Meta envoie un GET avec hub.verify_token et hub.challenge.
    Si le token correspond, on renvoie hub.challenge.
    """
    params = dict(request.query_params)
    mode      = params.get("hub.mode")
    token     = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook vérifié par Meta ✅")
        return Response(content=challenge, media_type="text/plain")

    logger.warning("Vérification webhook échouée — token: %s", token)
    raise HTTPException(status_code=403, detail="Token invalide")


@app.post("/webhook")
async def receive_webhook(request: Request) -> dict:
    """
    Réception des événements Messenger.
    Meta envoie les messages, quick replies et postbacks ici.
    """
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

            # Message texte ou quick reply
            if "message" in event and not event["message"].get("is_echo"):
                await handle_message(sender_id, event["message"])

            # Clic sur un bouton postback
            elif "postback" in event:
                await handle_postback(sender_id, event["postback"])

    # Meta attend toujours un 200 OK rapidement
    return {"status": "ok"}


@app.get("/health")
async def health() -> dict:
    return {
        "status":      "ok",
        "service":     "Nehanda Messenger Bot",
        "nehanda_url": NEHANDA_API_URL,
    }