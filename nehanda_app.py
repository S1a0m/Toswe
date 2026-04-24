# nehanda_app_gemini.py  — version 3.1  "Discovery First"
#
# Philosophie : Nehanda est un assistant de découverte et de conseil.
# Elle trouve, compare, explique et suggère.
# L'utilisateur garde la main sur le panier et la commande via l'app.
#
# Actions conservées :
#   - search_products           → recherche textuelle
#   - get_top_rated_products    → meilleurs produits par note
#   - get_product_status        → stock / promo / annonce
#   - compare_products          → comparaison multi-produits
#   - suggest_products_for_goal → liste produits pour un objectif
#   - get_product_price         → prix d'un produit
#   - track_order               → suivi de commande
#   - none                      → conversation générale
#
# Actions RETIRÉES (phase 1) :
#   - add_to_cart       → l'utilisateur le fait depuis l'app
#   - order_from_cart   → l'utilisateur le fait depuis l'app
#   - create_order      → idem
#
import os
import json
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Any

import jwt
import httpx

from google import genai
from google.genai import types
from google.api_core.exceptions import ResourceExhausted

from fastapi import FastAPI, Depends, HTTPException, Header, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

from nehanda_system_prompt import get_nehanda_system_prompt

from dotenv import load_dotenv
import os

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nehanda")

# ── Django bootstrap ──────────────────────────────────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      os.getenv("DJANGO_SETTINGS_MODULE", "toswe.settings"))
import django
django.setup()
from django.conf import settings as django_settings
from users.models import CustomUser

load_dotenv()

# ── Gemini ────────────────────────────────────────────────────
_gemini_key = os.getenv("GEMINI_API_KEY")
if not _gemini_key:
    raise RuntimeError("GEMINI_API_KEY manquante.")
gemini_client = genai.Client(api_key=_gemini_key)
GEMINI_MODEL  = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

MAX_MESSAGES_PER_CONVERSATION = int(os.getenv("MAX_MESSAGES_PER_CONV", "20"))
DRF_API_BASE = os.getenv("DRF_API_BASE", "http://127.0.0.1:8000/api")

# ── SQLAlchemy ────────────────────────────────────────────────
CONV_DB_URL = os.getenv("CONVERSATIONS_DB_URL", "sqlite:///./conversations.db")
engine = create_engine(
    CONV_DB_URL, future=True,
    connect_args={"check_same_thread": False} if CONV_DB_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    messages   = relationship("Message", back_populates="conversation",
                              cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    id              = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender          = Column(String(20), nullable=False)
    text            = Column(Text, nullable=False)
    created_at      = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    conversation    = relationship("Conversation", back_populates="messages")


Base.metadata.create_all(bind=engine)

# ═════════════════════════════════════════════════════════════
# Schémas Pydantic
# ═════════════════════════════════════════════════════════════

class ProductCard(BaseModel):
    """
    Carte produit enrichie retournée au Flutter.
    Contient tout ce qu'il faut pour afficher le produit
    et permettre à l'utilisateur de l'ajouter au panier lui-même.
    """
    id:                int
    name:              str
    price:             int
    image_url:         Optional[str]   = None
    rating_avg:        float           = 0.0
    rating_count:      int             = 0
    in_stock:          bool            = True
    has_promo:         bool            = False
    promo_percent:     Optional[int]   = None
    promo_price:       Optional[float] = None
    promo_ends_at:     Optional[str]   = None
    has_active_ad:     bool            = False
    shop_name:         Optional[str]   = None
    short_description: Optional[str]   = None
    description:       Optional[str]   = None        # ← nouveau
    category_name:     Optional[str]   = None   # ← nouveau


class ChatIn(BaseModel):
    message:         str
    conversation_id: Optional[int] = None

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Le message ne peut pas être vide.")
        if len(v) > 2000:
            raise ValueError("Message trop long (max 2000 caractères).")
        return v


class ChatOut(BaseModel):
    conversation_id:          int
    response:                 str
    new_conversation_started: bool              = False
    products:                 List[ProductCard] = []


class MessageOut(BaseModel):
    id: int; sender: str; text: str; created_at: datetime
    model_config = {"from_attributes": True}


class ConversationOut(BaseModel):
    id: int; user_id: Optional[int]; created_at: datetime
    messages: List[MessageOut]
    model_config = {"from_attributes": True}


class ConversationSummary(BaseModel):
    id: int; created_at: datetime; message_count: int
    first_user_message: Optional[str] = None
    model_config = {"from_attributes": True}


class AIDecision(BaseModel):
    intent:     str
    action:     str
    parameters: dict[str, Any] = {}
    response:   str


BASE_URL = "http://192.168.1.84:8000"

def _full_image_url(path: str | None) -> str | None:
    if not path:
        return None
    # Normalise les URLs localhost vers l'IP réseau
    if "127.0.0.1" in path or "localhost" in path:
        from urllib.parse import urlparse
        parsed = urlparse(path)
        path = path.replace(f"{parsed.scheme}://{parsed.netloc}", BASE_URL)
        return path
    if path.startswith("http"):
        return path
    clean = path.lstrip("/")
    if not clean.startswith("media/"):
        clean = f"media/{clean}"
    return f"{BASE_URL}/{clean}"

# ═════════════════════════════════════════════════════════════
# Helper : dict produit Django → ProductCard
# ═════════════════════════════════════════════════════════════

def _build_product_card(p: dict) -> ProductCard:
    main_img  = p.get("main_image")
    print("DEBUG main_image:", main_img)
    if isinstance(main_img, dict):
        raw_url = main_img.get("image")
    else:
        raw_url = main_img  # string directe ou None
    image_url = _full_image_url(raw_url)
    rating    = p.get("total_rating") or {}
    promotion = p.get("promotion")    or {}
    shop_name = (
        p.get("shop_name")
        or (p.get("seller") or {}).get("shop_name")
    )

    return ProductCard(
        id                = p["id"],
        name              = p["name"],
        price             = int(p.get("price", 0)),
        image_url         = image_url,
        rating_avg        = float(rating.get("average", 0)),
        rating_count      = int(rating.get("count", 0)),
        in_stock          = p.get("in_stock", True),
        has_promo         = bool(promotion),
        promo_percent     = promotion.get("discount_percent") if promotion else None,
        promo_price       = float(promotion["discount_price"])
                            if promotion and promotion.get("discount_price") else None,
        promo_ends_at     = str(promotion["ended_at"])[:10]
                            if promotion and promotion.get("ended_at") else None,
        has_active_ad     = p.get("is_sponsored", False),
        shop_name         = shop_name,
        short_description = p.get("short_description"),
        description       = p.get("description"),        # ← nouveau
        category_name     = p.get("category_name"),      # ← nouveau
    )

# ═════════════════════════════════════════════════════════════
# Dependencies FastAPI
# ═════════════════════════════════════════════════════════════

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _extract_token(authorization: Optional[str],
                   cookie_token:  Optional[str]) -> Optional[str]:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    return cookie_token or None


def get_optional_user(
    authorization: Optional[str] = Header(None),
    access_token:  Optional[str] = Cookie(None),
) -> Optional[CustomUser]:
    token = _extract_token(authorization, access_token)
    if not token:
        return None
    try:
        payload = jwt.decode(token, django_settings.SECRET_KEY, algorithms=["HS256"])
        email   = payload.get("email")
        if not email:
            return None
        return CustomUser.objects.get(email=email)
    except Exception:
        return None


def get_current_user(
    authorization: Optional[str] = Header(None),
    access_token:  Optional[str] = Cookie(None),
) -> CustomUser:
    user = get_optional_user(authorization, access_token)
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

# ═════════════════════════════════════════════════════════════
# Tools  — tous retournent (texte: str, cartes: List[ProductCard])
# ═════════════════════════════════════════════════════════════

# ── Recherche textuelle ───────────────────────────────────────
async def tool_search_products(
    query: str = "", max_price: Optional[int] = None, **_
) -> tuple[str, List[ProductCard]]:
    params: dict[str, Any] = {"q": query}
    if max_price:
        params["max_price"] = max_price
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get(f"{DRF_API_BASE}/product/search_products/", params=params)
            r.raise_for_status()
            raw = r.json()
        print("RAW SEARCH:", raw)
        products = raw if isinstance(raw, list) else raw.get("results", [])
        print("PARSED PRODUCTS:", products)
        if not products:
            return "Aucun produit trouvé pour cette recherche. 😔", []
        cards = [_build_product_card(p) for p in products[:6]]
        lines = [
            f"• **{c.name}** — {c.price} CFA"
            + (f" 🏷️ -{c.promo_percent}%" if c.has_promo else "")
            + ("" if c.in_stock else " *(épuisé)*")
            for c in cards
        ]
        return "Voici ce que j'ai trouvé :\n" + "\n".join(lines), cards
    except Exception as exc:
        logger.warning("tool_search_products: %s", exc)
        return "Je n'ai pas pu récupérer les produits. Réessaie !", []


# ── Meilleurs produits par note ───────────────────────────────
async def tool_get_top_rated_products(
    query: str = "", category: str = "", limit: int = 5, **_
) -> tuple[str, List[ProductCard]]:
    params: dict[str, Any] = {"q": query or category or ""}
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get(f"{DRF_API_BASE}/product/search_products/", params=params)
            r.raise_for_status()
            raw = r.json()
        products = raw if isinstance(raw, list) else raw.get("results", [])
        products.sort(
            key=lambda p: float((p.get("total_rating") or {}).get("average", 0)),
            reverse=True,
        )
        products = products[:limit]
        if not products:
            return "Aucun produit trouvé dans cette catégorie. 😔", []
        cards = [_build_product_card(p) for p in products]
        lines = []
        for c in cards:
            note  = f"⭐ {c.rating_avg}/5 ({c.rating_count} avis)"
            promo = f" 🏷️ -{c.promo_percent}% → {int(c.promo_price or 0)} CFA" if c.has_promo else ""
            stock = "" if c.in_stock else " ⚠️ *Épuisé*"
            lines.append(f"• **{c.name}** — {c.price} CFA | {note}{promo}{stock}")
        return "🌟 Meilleurs produits par note :\n" + "\n".join(lines), cards
    except Exception as exc:
        logger.warning("tool_get_top_rated_products: %s", exc)
        return "Impossible de récupérer les produits.", []


# ── Statut complet d'un produit ───────────────────────────────
async def tool_get_product_status(
    product_id: Optional[int] = None, product_name: str = "", **_
) -> tuple[str, List[ProductCard]]:
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            if product_id:
                r = await c.get(f"{DRF_API_BASE}/product/{product_id}/")
            else:
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": product_name})
            r.raise_for_status()
            raw = r.json()

        p = raw if product_id else (
            (raw if isinstance(raw, list) else raw.get("results", []) or [{}])[0]
        )
        if not p:
            return "Produit introuvable. Vérifie le nom ou l'identifiant.", []

        card  = _build_product_card(p)
        parts = [f"📦 **{card.name}** — {card.price} CFA"]
        parts.append("✅ En stock" if card.in_stock else "❌ Épuisé — indisponible actuellement")

        if card.has_promo:
            ends = f" (jusqu'au {card.promo_ends_at})" if card.promo_ends_at else ""
            parts.append(
                f"🏷️ Promotion active : -{card.promo_percent}% "
                f"→ **{int(card.promo_price or 0)} CFA**{ends}"
            )
        else:
            parts.append("Aucune promotion en cours.")

        if card.has_active_ad:
            parts.append("📢 Produit mis en avant via une annonce sponsorisée.")

        return "\n".join(parts), [card]
    except Exception as exc:
        logger.warning("tool_get_product_status: %s", exc)
        return "Je n'ai pas pu récupérer le statut de ce produit.", []


# ── Comparaison multi-produits ────────────────────────────────
async def tool_compare_products(
    product_ids:   Optional[List[int]] = None,
    product_names: Optional[List[str]] = None,
    **_,
) -> tuple[str, List[ProductCard]]:

    async def _fetch_one(cid: Optional[int], name: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient(timeout=8) as c:
                if cid:
                    r = await c.get(f"{DRF_API_BASE}/product/{cid}/")
                    r.raise_for_status()
                    return r.json()
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": name})
                r.raise_for_status()
                raw = r.json()
                lst = raw if isinstance(raw, list) else raw.get("results", [])
                return lst[0] if lst else None
        except Exception:
            return None

    ids   = product_ids   or []
    names = product_names or []
    pairs = [
        (ids[i]   if i < len(ids)   else None,
         names[i] if i < len(names) else "")
        for i in range(max(len(ids), len(names)))
    ]
    results  = await asyncio.gather(*[_fetch_one(cid, nm) for cid, nm in pairs])
    products = [p for p in results if p]

    if not products:
        return "Je n'ai pas trouvé les produits à comparer. Précise les noms ou IDs.", []

    cards = [_build_product_card(p) for p in products]
    lines = ["📊 **Comparaison de produits** :\n"]
    for c in cards:
        note  = f"⭐ {c.rating_avg}/5 ({c.rating_count} avis)"
        promo = (f"🏷️ -{c.promo_percent}% → {int(c.promo_price or 0)} CFA"
                 if c.has_promo else "Aucune promo")
        stock = "✅ En stock" if c.in_stock else "❌ Épuisé"
        lines.append(
            f"**{c.name}**\n"
            f"  Prix    : {c.price} CFA | {promo}\n"
            f"  Note    : {note}\n"
            f"  Stock   : {stock}\n"
            + (f"  Boutique : {c.shop_name}\n" if c.shop_name else "")
            + (f"  _{c.short_description}_\n"   if c.short_description else "")
        )
    best = max(cards, key=lambda c: (c.rating_avg, -c.price))
    lines.append(f"\n🏆 Mon conseil : **{best.name}** — meilleur rapport qualité/prix.")
    return "\n".join(lines), cards


# ── Suggestions par objectif ──────────────────────────────────
async def tool_suggest_products_for_goal(
    goal: str = "", keywords: Optional[List[str]] = None, **_
) -> tuple[str, List[ProductCard]]:
    if not goal and not keywords:
        return "Décris-moi ton objectif et je trouve les produits pour toi !", []

    search_terms = keywords or [goal]

    async def _search(term: str) -> List[dict]:
        try:
            async with httpx.AsyncClient(timeout=8) as c:
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": term})
                r.raise_for_status()
                raw = r.json()
                lst = raw if isinstance(raw, list) else raw.get("results", [])
                return lst[:2]
        except Exception:
            return []

    all_results = await asyncio.gather(*[_search(t) for t in search_terms])

    seen: set[int] = set()
    products: List[dict] = []
    for batch in all_results:
        for p in batch:
            if p.get("id") not in seen:
                seen.add(p["id"])
                products.append(p)

    if not products:
        return (
            f"Je n'ai pas encore de produits pour « {goal} » sur la plateforme. "
            f"Nos vendeurs enrichissent le catalogue chaque jour ! 🌍",
            [],
        )

    cards = [_build_product_card(p) for p in products]
    intro = f"Pour **{goal}**, voici ce que je te propose 🎯 :\n"
    lines = [
        f"• **{c.name}** — {c.price} CFA"
        + (f" 🏷️ -{c.promo_percent}%" if c.has_promo else "")
        + ("" if c.in_stock else " *(épuisé)*")
        for c in cards
    ]
    return intro + "\n".join(lines), cards


# ── Prix d'un produit ─────────────────────────────────────────
async def tool_get_price(
    product_name: str = "", product_id: Optional[int] = None, **_
) -> tuple[str, List[ProductCard]]:
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            if product_id:
                r = await c.get(f"{DRF_API_BASE}/product/{product_id}/")
                r.raise_for_status()
                p = r.json()
            else:
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": product_name})
                r.raise_for_status()
                raw = r.json()
                lst = raw if isinstance(raw, list) else raw.get("results", [])
                p   = lst[0] if lst else None
        if not p:
            return "Produit introuvable. Vérifie le nom ou l'identifiant.", []
        card = _build_product_card(p)
        promo_info = (
            f" (promo : {int(card.promo_price or 0)} CFA 🏷️)" if card.has_promo else ""
        )
        return (
            f"Le prix de **{card.name}** est de **{card.price} CFA**{promo_info}. 💵",
            [card],
        )
    except Exception as exc:
        logger.warning("tool_get_price: %s", exc)
        return "Je n'ai pas pu récupérer le prix.", []


# ── Nouveautés et promos ──────────────────────────────────────
async def tool_get_new_and_promos(**_) -> tuple[str, List[ProductCard]]:
    """
    Retourne les nouveautés (status=new) et les produits en promo active.
    Utile pour répondre à "quelles sont vos nouveautés / vos promos ?"
    """
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            # Nouveautés
            r_new = await c.get(
                f"{DRF_API_BASE}/product/suggestions/",
                params={"limit": 6}
            )
            r_new.raise_for_status()
            raw_new = r_new.json()

        products = raw_new if isinstance(raw_new, list) else raw_new.get("results", [])
        if not products:
            return "Pas encore de nouveautés sur la plateforme 😔", []

        cards = [_build_product_card(p) for p in products[:8]]

        # Sépare nouveautés et promos
        promos   = [c for c in cards if c.has_promo]
        new_ones = [c for c in cards if not c.has_promo]

        parts = []

        if promos:
            parts.append("🏷️ **Promotions en cours** :")
            for c in promos:
                parts.append(
                    f"• **{c.name}** — ~~{c.price} CFA~~ → "
                    f"**{int(c.promo_price or c.price)} CFA** "
                    f"(-{c.promo_percent}%)"
                    + (f" ⏰ jusqu'au {c.promo_ends_at}" if c.promo_ends_at else "")
                )

        if new_ones:
            parts.append("\n✨ **Nouveautés** :")
            for c in new_ones[:4]:
                parts.append(
                    f"• **{c.name}** — {c.price} CFA"
                    + ("" if c.in_stock else " *(épuisé)*")
                )

        return "\n".join(parts), cards

    except Exception as exc:
        logger.warning("tool_get_new_and_promos: %s", exc)
        return "Je n'ai pas pu récupérer les nouveautés. Réessaie !", []


# ── Passer une commande via Nehanda (Messenger / chat) ────────
async def tool_create_order(
    product_name:       str = "",
    product_id:         Optional[int] = None,
    quantity:           int = 1,
    phone_number:       str = "",
    contact_method:     str = "call",     # "call" | "whatsapp"
    city:               str = "",
    address_description: str = "",
    delivery_mode:      str = "home",     # "home" | "relay"
    **_
) -> tuple[str, List[ProductCard]]:
    """
    Passe une commande directement depuis Nehanda.
    Utilisé principalement depuis Messenger quand le client
    donne tous les détails en conversation.

    Flux :
    1. Trouve le produit si pas d'ID fourni
    2. Valide les champs obligatoires
    3. Poste la commande sur l'API Django
    4. Retourne la confirmation avec le numéro de commande
    """

    # ── 1. Validation des champs obligatoires ─────────────────
    missing = []
    if not phone_number or len(phone_number.strip()) < 8:
        missing.append("ton numéro de téléphone")
    if not city.strip() and delivery_mode == "home":
        missing.append("ta ville de livraison")
    if missing:
        return (
            f"Pour finaliser ta commande, j'ai besoin de : {', '.join(missing)}. "
            f"Peux-tu me les donner ? 😊",
            []
        )

    # ── 2. Résolution du produit ──────────────────────────────
    if not product_id and product_name:
        try:
            async with httpx.AsyncClient(timeout=8) as c:
                r = await c.get(
                    f"{DRF_API_BASE}/product/search_products/",
                    params={"q": product_name}
                )
                r.raise_for_status()
                raw = r.json()
            lst = raw if isinstance(raw, list) else raw.get("results", [])
            if not lst:
                return (
                    f"Je n'ai pas trouvé de produit nommé « {product_name} » 😔 "
                    f"Peux-tu préciser le nom exact ?",
                    []
                )
            product_id = lst[0]["id"]
        except Exception as exc:
            logger.warning("tool_create_order — recherche produit: %s", exc)
            return "Je n'ai pas pu trouver ce produit. Réessaie !", []

    if not product_id:
        return "Précise le nom ou l'identifiant du produit que tu veux commander.", []

    # ── 3. Appel API Django ───────────────────────────────────
    payload = {
        "phone_number":        phone_number.strip(),
        "contact_method":      contact_method,
        "city":                city.strip() if delivery_mode == "home" else "Point relais",
        "address_description": address_description.strip(),
        "delivery_mode":       delivery_mode,
        "items": [
            {"product_id": product_id, "quantity": quantity}
        ],
    }

    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{DRF_API_BASE}/order/",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            r.raise_for_status()
            data = r.json()

        order_id = data.get("id", "?")

        return (
            f"✅ **Commande #{order_id} enregistrée !**\n\n"
            f"Notre équipe va te contacter au **{phone_number}** "
            f"({'WhatsApp' if contact_method == 'whatsapp' else 'appel'}) "
            f"pour confirmer la livraison.\n\n"
            f"🛡️ Tu ne seras débité qu'à la réception.\n"
            f"📦 Garde ce numéro : **#{order_id}** pour suivre ta commande.",
            []
        )

    except httpx.HTTPStatusError as exc:
        logger.warning("tool_create_order — API: %s — %s", exc.response.status_code, exc.response.text)
        try:
            detail = exc.response.json().get("detail", "Erreur inconnue")
        except Exception:
            detail = "Erreur serveur"
        return f"Je n'ai pas pu enregistrer ta commande 😔 : {detail}", []
    except Exception as exc:
        logger.warning("tool_create_order: %s", exc)
        return "Une erreur s'est produite. Réessaie dans quelques instants !", []


# ── Suivi de commande ─────────────────────────────────────────
async def tool_track_order(
    order_id: Optional[int] = None, **_
) -> tuple[str, List[ProductCard]]:
    if not order_id:
        return "Donne-moi ton numéro de commande (ex: #1234). 📦", []
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get(f"{DRF_API_BASE}/order/{order_id}/")
            r.raise_for_status()
            order = r.json()
        STATUS_FR = {
            "pending":   "En attente ⏳",
            "confirmed": "Confirmée ✅",
            "shipped":   "En livraison 🚴",
            "delivered": "Livrée 🎉",
            "cancelled": "Annulée ❌",
        }
        label = STATUS_FR.get(order.get("status", ""), order.get("status", ""))
        return f"📦 Commande **#{order['id']}** — Statut : **{label}**", []
    except Exception as exc:
        logger.warning("tool_track_order: %s", exc)
        return "Je n'ai pas pu trouver cette commande. Vérifie le numéro.", []


async def tool_none(**_) -> tuple[str, List[ProductCard]]:
    return "", []

# ═════════════════════════════════════════════════════════════
# Registry
# ═════════════════════════════════════════════════════════════
TOOL_REGISTRY: dict[str, Any] = {
    "search_products":           tool_search_products,
    "get_top_rated_products":    tool_get_top_rated_products,
    "get_product_status":        tool_get_product_status,
    "compare_products":          tool_compare_products,
    "suggest_products_for_goal": tool_suggest_products_for_goal,
    "get_product_price":         tool_get_price,
    "track_order":               tool_track_order,
    "get_new_and_promos":        tool_get_new_and_promos,   # ← nouveau
    "create_order":              tool_create_order,          # ← nouveau
    "none":                      tool_none,
}

_AVAILABLE_ACTIONS = ", ".join(f'"{k}"' for k in TOOL_REGISTRY)

# ═════════════════════════════════════════════════════════════
# System prompt
# ═════════════════════════════════════════════════════════════
NEHANDA_SYSTEM_PROMPT = get_nehanda_system_prompt(_AVAILABLE_ACTIONS)

NEHANDA_SYSTEM_PROMPT += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHILOSOPHIE DISCOVERY FIRST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tu es une assistante de découverte et de conseil.
Tu trouves, compares, expliques et suggères des produits.
L'utilisateur garde TOUJOURS la main sur le panier et la commande via l'app.

Tu ne dois JAMAIS prétendre ajouter au panier ou passer une commande.
Si l'utilisateur demande à commander ou ajouter au panier, tu dois :
1. Lui montrer le(s) produit(s) concerné(s) via les actions disponibles.
2. L'inviter à utiliser le bouton "Ajouter au panier" ou "Commander" dans l'app.

Si une recherche ou une promo ne donne rien, ne dis pas juste 'je n'ai rien'. Propose de chercher autre chose ou demande au client ce qu'il veut cuisiner/faire aujourd'hui.

Exemple :
Message : "ajoute l'huile de palme à mon panier"
{"intent":"cart_redirect","action":"search_products","parameters":{"query":"huile de palme"},
 "response":"Je t'ai trouvé les huiles de palme disponibles 🫒 ! Appuie sur le bouton \\"Ajouter au panier\\" sur la carte du produit qui t'intéresse 🛒"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIONS DISPONIBLES — DÉTAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- "search_products"           → Recherche textuelle avec filtre prix optionnel.
                                 Params : query (str), max_price (int, optionnel)

- "get_top_rated_products"    → Produits triés par meilleure note client.
                                 Signale promos actives et ruptures de stock.
                                 Params : query (str), category (str), limit (int, défaut 5)

- "get_product_status"        → État complet d'un produit : stock, promo, annonce.
                                 Params : product_id (int) OU product_name (str)

- "compare_products"          → Compare prix, note, promo, stock, description.
                                 Params : product_ids (list[int]) OU product_names (list[str])

- "suggest_products_for_goal" → Suggère une liste de produits pour un objectif précis.
                                 Params : goal (str), keywords (list[str])
                                 Exemples : "meubler ma chambre", "tenue gala africain",
                                 "cuisine africaine", "saison des pluies au Bénin".

- "get_product_price"         → Prix d'un produit avec info promo si applicable.
                                 Params : product_name (str) OU product_id (int)

- "get_new_and_promos"  → Retourne les nouveautés et promotions actives.
                           Params : aucun
                           Utilise quand le client demande :
                           "quelles sont vos nouveautés ?", "vous avez des promos ?",
                           "qu'est-ce qui est nouveau ?", "quelles offres en ce moment ?"

- "create_order"        → Passe une commande directement via Nehanda.
                           UTILISE SEULEMENT quand le client donne TOUS les détails
                           nécessaires : produit, téléphone, ville/adresse.
                           Si des infos manquent → demande-les avant d'appeler.
                           Params :
                             product_name (str) OU product_id (int)
                             quantity (int, défaut 1)
                             phone_number (str) — OBLIGATOIRE
                             contact_method (str) — "call" ou "whatsapp"
                             city (str) — OBLIGATOIRE si delivery_mode="home"
                             address_description (str) — point de repère
                             delivery_mode (str) — "home" ou "relay"

- "track_order"               → Suivi de commande par numéro.
                                 Params : order_id (int)

- "none"                      → Conversation générale, infos plateforme, aide.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXEMPLES COMPLETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Message : "montre-moi les meilleures huiles"
{"intent":"top_rated","action":"get_top_rated_products","parameters":{"query":"huile","limit":5},"response":"Voici les huiles les mieux notées par nos clients 🌟..."}

Message : "compare le tissu wax et le pagne"
{"intent":"compare","action":"compare_products","parameters":{"product_names":["tissu wax","pagne"]},"response":"Je compare ces deux produits pour toi 📊..."}

Message : "le savon karité est-il en stock ?"
{"intent":"product_status","action":"get_product_status","parameters":{"product_name":"savon karité"},"response":"Je vérifie le statut du savon karité 📦..."}

Message : "je vais à un gala africain, qu'est-ce que je mets ?"
{"intent":"goal_suggestion","action":"suggest_products_for_goal","parameters":{"goal":"tenue gala africain","keywords":["boubou","robe africaine","pagne","tissu wax","accessoires africains"]},"response":"Pour un gala africain tu dois être éblouissant(e) ✨ ! Voici mes suggestions — utilise le bouton Ajouter au panier sur ce qui te plaît 🛒"}

Message : "j'aménage ma chambre, de quoi j'ai besoin ?"
{"intent":"goal_suggestion","action":"suggest_products_for_goal","parameters":{"goal":"aménager une chambre","keywords":["lit","matelas","draps","coussin","lampe","étagère","rideau"]},"response":"Pour une belle chambre 🛏️, voici ce que je te propose sur Tôswè. Ajoute ce qui t'intéresse directement depuis l'app !"}

Message : "ajoute l'huile de palme à mon panier"
{"intent":"cart_redirect","action":"search_products","parameters":{"query":"huile de palme"},"response":"Je t'ai trouvé les huiles de palme disponibles 🫒 ! Appuie sur le bouton \\"Ajouter au panier\\" sur la carte du produit qui t'intéresse 🛒"}

Message : "quelles tenues pour la saison des pluies ?"
{"intent":"goal_suggestion","action":"suggest_products_for_goal","parameters":{"goal":"tenue saison pluvieuse","keywords":["imperméable","bottes","parapluie","tenue légère"]},"response":"Pour la saison des pluies au Bénin ☔, voici mes recommandations..."}

Message : "quel est le prix de l'huile de coco ?"
{"intent":"price_check","action":"get_product_price","parameters":{"product_name":"huile de coco"},"response":"Je vérifie le prix de l'huile de coco pour toi 💵..."}

Message : "je veux commander 2 savons karité, mon numéro c'est 97000000, je suis à Cotonou Akpakpa"
{"intent":"direct_order","action":"create_order","parameters":{"product_name":"savon karité","quantity":2,"phone_number":"97000000","city":"Cotonou","address_description":"Akpakpa","delivery_mode":"home","contact_method":"call"},"response":"Je passe ta commande tout de suite 🛒..."}

Message : "quelles sont vos nouveautés ?"
{"intent":"new_and_promos","action":"get_new_and_promos","parameters":{},"response":"Voici ce qui vient d'arriver sur Tôswè ✨ !"}
"""

# ═════════════════════════════════════════════════════════════
# Gemini helpers
# ═════════════════════════════════════════════════════════════

def _to_gemini_history(history: list[dict]) -> list[types.Content]:
    turns: list[types.Content] = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        text = msg.get("content", "")
        if turns and turns[-1].role == role:
            existing = turns[-1].parts[0].text or ""
            turns[-1] = types.Content(role=role,
                                      parts=[types.Part(text=existing + "\n" + text)])
        else:
            turns.append(types.Content(role=role, parts=[types.Part(text=text)]))
    return turns


async def nehanda_ask_gemini(
    message: str, history: list[dict] | None = None
) -> AIDecision:
    history = history or []
    config  = types.GenerateContentConfig(
        system_instruction=NEHANDA_SYSTEM_PROMPT,
        temperature=0.3,
        max_output_tokens=768,
        response_mime_type="application/json",
    )
    response = await gemini_client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=_to_gemini_history(history) + [
            types.Content(role="user", parts=[types.Part(text=message)])
        ],
        config=config,
    )
    raw = (response.text or "").strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw   = parts[1][4:] if parts[1].startswith("json") else parts[1]
        raw   = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON invalide: {raw!r}") from exc

    missing = [f for f in ("intent", "action", "response") if f not in data]
    if missing:
        raise ValueError(f"Champs manquants {missing}")

    if data["action"] not in TOOL_REGISTRY:
        logger.warning("Action inconnue '%s' → fallback 'none'", data["action"])
        data["action"] = "none"

    return AIDecision(
        intent    =str(data["intent"]),
        action    =str(data["action"]),
        parameters=data.get("parameters") or {},
        response  =str(data["response"]),
    )

# ═════════════════════════════════════════════════════════════
# Brain
# ═════════════════════════════════════════════════════════════

async def nehanda_brain_reply(
    message: str,
    db:      Session,
    conv_id: int,
) -> tuple[str, List[ProductCard]]:
    raw_msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .order_by(Message.id.desc()).limit(10).all()
    )
    history = [
        {"role": "assistant" if m.sender == "nehanda" else "user",
         "content": m.text}
        for m in reversed(raw_msgs)
    ]

    try:
        decision = await nehanda_ask_gemini(message, history)
    except ResourceExhausted as exc:
        logger.warning("Quota Gemini: %s", exc)
        return (
            "Je suis temporairement indisponible 😔 — quota API dépassé. "
            "Réessaie dans quelques minutes.",
            [],
        )
    except ValueError as exc:
        logger.error("Parsing Gemini: %s", exc)
        return "Je n'ai pas bien compris 😕. Peux-tu reformuler ?", []

    logger.info("intent=%s action=%s params=%s",
                decision.intent, decision.action, decision.parameters)

    tool_fn = TOOL_REGISTRY.get(decision.action, tool_none)

    try:
        tool_result, cards = await tool_fn(**decision.parameters)
    except Exception as exc:
        logger.exception("Tool '%s' erreur: %s", decision.action, exc)
        tool_result, cards = "", []

    if tool_result and decision.action != "none":
        return f"{decision.response}\n\n{tool_result}", cards

    return decision.response, cards

# ═════════════════════════════════════════════════════════════
# App lifespan
# ═════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Nehanda v3.1 'Discovery First' | Model: %s | Tools: %s",
                GEMINI_MODEL, list(TOOL_REGISTRY.keys()))
    yield
    logger.info("Nehanda arrêtée.")

# ═════════════════════════════════════════════════════════════
# FastAPI
# ═════════════════════════════════════════════════════════════

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000,http://192.168.46.69,http://192.168.1.70",
).split(",")

app = FastAPI(title="Nehanda — Discovery First", version="3.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═════════════════════════════════════════════════════════════
# Endpoints
# ═════════════════════════════════════════════════════════════

@app.post("/refresh_token")
def refresh_token(
    refresh_token_cookie: Optional[str] = Cookie(None, alias="refresh_token"),
):
    if not refresh_token_cookie:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        payload = jwt.decode(refresh_token_cookie,
                             django_settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid payload")
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "access": jwt.encode(
            {"email": user.email,
             "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
            django_settings.SECRET_KEY,
            algorithm="HS256",
        )
    }


@app.post("/nehanda/chat", response_model=ChatOut)
async def chat_with_nehanda(
    payload:       ChatIn,
    db:            Session              = Depends(get_db),
    current_user:  Optional[CustomUser] = Depends(get_optional_user),
):
    new_conversation_started = False
    conv: Optional[Conversation] = None

    # ── Résolution conversation ──────────────────────────────
    if payload.conversation_id:
        conv = db.get(Conversation, payload.conversation_id)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if current_user and conv.user_id and conv.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access forbidden")

    if conv is None:
        if current_user:
            conv = (
                db.query(Conversation)
                .filter(Conversation.user_id == current_user.id)
                .with_for_update()
                .order_by(Conversation.id.desc())
                .first()
            )
        if conv is None:
            conv = Conversation(user_id=current_user.id if current_user else None)
            db.add(conv)
            db.flush()

    # ── Limite messages ──────────────────────────────────────
    if current_user:
        msg_count = (db.query(Message)
                       .filter(Message.conversation_id == conv.id)
                       .count())
        if msg_count >= MAX_MESSAGES_PER_CONVERSATION:
            conv = Conversation(user_id=current_user.id)
            db.add(conv)
            db.flush()
            new_conversation_started = True
            logger.info("Nouvelle conversation auto (user=%s)", current_user.id)

    db.add(Message(conversation_id=conv.id, sender="user", text=payload.message))

    # ── Brain ────────────────────────────────────────────────
    try:
        reply, cards = await nehanda_brain_reply(payload.message, db, conv.id)
    except Exception as exc:
        db.rollback()
        logger.exception("Erreur brain: %s", exc)
        raise HTTPException(status_code=500, detail="Erreur interne de Nehanda.")

    db.add(Message(conversation_id=conv.id, sender="nehanda", text=reply))
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.exception("Erreur commit: %s", exc)
        raise HTTPException(status_code=500, detail="Erreur de sauvegarde.")

    return ChatOut(
        conversation_id=conv.id,
        response=reply,
        new_conversation_started=new_conversation_started,
        products=cards,
    )


@app.get("/conversations/list", response_model=List[ConversationSummary])
def list_conversations(
    db:     Session    = Depends(get_db),
    user:   CustomUser = Depends(get_current_user),
    limit:  int = 50,
    offset: int = 0,
):
    convs = (
        db.query(Conversation)
        .filter(Conversation.user_id == user.id)
        .order_by(Conversation.created_at.desc())
        .offset(offset).limit(limit).all()
    )
    result = []
    for conv in convs:
        msgs = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.id.asc()).all()
        )
        first_user_msg = next((m.text for m in msgs if m.sender == "user"), None)
        result.append(ConversationSummary(
            id=conv.id, created_at=conv.created_at,
            message_count=len(msgs), first_user_message=first_user_msg,
        ))
    return result


@app.get("/conversations/{conversation_id}", response_model=ConversationOut)
def get_conversation(
    conversation_id: int,
    db:              Session    = Depends(get_db),
    user:            CustomUser = Depends(get_current_user),
):
    conv = db.get(Conversation, conversation_id)
    if not conv or conv.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.id.asc()).all()
    )
    return ConversationOut(
        id=conv.id, user_id=conv.user_id, created_at=conv.created_at,
        messages=[MessageOut(id=m.id, sender=m.sender, text=m.text,
                             created_at=m.created_at) for m in msgs],
    )


 # réexporte tout

# ═════════════════════════════════════════════════════════════
# PATCH CLOSING — Fonctions enrichies avec signaux d'urgence
# Remplace les tools originaux dans TOOL_REGISTRY après import.
# ═════════════════════════════════════════════════════════════

from datetime import datetime, timezone as tz
from typing import Optional, List
import httpx
import logging

logger = logging.getLogger("nehanda.closing")

# ── Helpers signaux urgence ───────────────────────────────────

def _promo_urgency(card: "ProductCard") -> str:
    """
    Retourne une ligne de signal d'urgence liée à la promo,
    ou chaîne vide si pas de promo.
    """
    if not card.has_promo:
        return ""

    parts = []

    if card.promo_percent:
        parts.append(f"🏷️ -{card.promo_percent}% en ce moment — c'est rare, profites-en !")

    if card.promo_ends_at:
        try:
            ends = datetime.strptime(card.promo_ends_at, "%Y-%m-%d")
            delta = (ends - datetime.now()).days
            if delta == 0:
                parts.append("⏰ Promo expire **aujourd'hui** — c'est maintenant ou jamais !")
            elif delta == 1:
                parts.append("⏰ Promo expire **demain** — dépêche-toi !")
            elif delta <= 3:
                parts.append(f"⏰ Promo expire dans **{delta} jours** — encore un peu de temps !")
            elif delta <= 7:
                parts.append(f"⏰ Promo valable encore **{delta} jours**.")
        except ValueError:
            pass

    return " ".join(parts)


def _stock_urgency(card: "ProductCard") -> str:
    """Signal stock bas — uniquement si hors stock (on ne ment pas sur 'peu de stock')."""
    if not card.in_stock:
        return "⚠️ Ce produit est actuellement **épuisé** — surveille la boutique pour être alerté !"
    return ""


def _rating_signal(card: "ProductCard") -> str:
    """Signal note client si significatif."""
    if card.rating_count >= 3 and card.rating_avg >= 4.0:
        return f"⭐ {card.rating_avg}/5 avec {card.rating_count} avis clients — les acheteurs adorent !"
    return ""


def _closing_line(card: "ProductCard") -> str:
    """
    Ligne de closing final adaptée au contexte du produit.
    Priorité : promo > note > défaut.
    """
    if card.has_promo and card.promo_ends_at:
        try:
            ends = datetime.strptime(card.promo_ends_at, "%Y-%m-%d")
            delta = (ends - datetime.now()).days
            if delta <= 3:
                return "👉 C'est le bon moment — appuie sur **Ajouter au panier** sur la carte 🛒"
        except ValueError:
            pass
    if card.rating_avg >= 4.5 and card.rating_count >= 5:
        return "👉 Les clients valident — vas-y, tu vas pas regretter 🛒"
    return "👉 Tu n'es qu'à 2 clics de le recevoir chez toi 🛒"


def _urgency_block(card: "ProductCard") -> str:
    """
    Assemble tous les signaux disponibles pour un produit.
    Retourne un bloc texte (peut être vide).
    """
    signals = [s for s in [
        _promo_urgency(card),
        _stock_urgency(card),
        _rating_signal(card),
    ] if s]
    return "\n".join(signals)


# ── Tool : search_products (closing enrichi) ─────────────────

async def tool_search_products_closing(
    query: str = "", max_price: Optional[int] = None, **_
) -> tuple[str, List["ProductCard"]]:
    params: dict = {"q": query}
    if max_price:
        params["max_price"] = max_price
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get(f"{DRF_API_BASE}/product/search_products/", params=params)
            r.raise_for_status()
            raw = r.json()
        products = raw if isinstance(raw, list) else raw.get("results", [])
        if not products:
            return "Aucun produit trouvé pour cette recherche. 😔", []
        cards = [_build_product_card(p) for p in products[:6]]

        lines = []
        for card in cards:
            line = f"• **{card.name}** — {card.price} CFA"
            if card.has_promo and card.promo_price:
                line += f" ~~{card.price}~~ → **{int(card.promo_price)} CFA** 🏷️"
            if not card.in_stock:
                line += " *(épuisé)*"
            urgency = _urgency_block(card)
            if urgency:
                line += f"\n  {urgency}"
            lines.append(line)

        # Si un seul résultat très pertinent → closing direct
        if len(cards) == 1:
            lines.append(f"\n{_closing_line(cards[0])}")

        return "Voici ce que j'ai trouvé 🌍 :\n" + "\n".join(lines), cards
    except Exception as exc:
        logger.warning("tool_search_products_closing: %s", exc)
        return "Je n'ai pas pu récupérer les produits. Réessaie !", []


# ── Tool : get_top_rated_products (closing enrichi) ──────────

async def tool_get_top_rated_closing(
    query: str = "", category: str = "", limit: int = 5, **_
) -> tuple[str, List["ProductCard"]]:
    params: dict = {"q": query or category or ""}
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            r = await c.get(f"{DRF_API_BASE}/product/search_products/", params=params)
            r.raise_for_status()
            raw = r.json()
        products = raw if isinstance(raw, list) else raw.get("results", [])
        products.sort(
            key=lambda p: float((p.get("total_rating") or {}).get("average", 0)),
            reverse=True,
        )
        products = products[:limit]
        if not products:
            return "Aucun produit trouvé dans cette catégorie. 😔", []

        cards = [_build_product_card(p) for p in products]
        lines = []
        for i, card in enumerate(cards):
            note = f"⭐ {card.rating_avg}/5 ({card.rating_count} avis)"
            promo = f" 🏷️ -{card.promo_percent}% → {int(card.promo_price or 0)} CFA" if card.has_promo else ""
            stock = "" if card.in_stock else " ⚠️ *Épuisé*"
            line = f"• **{card.name}** — {card.price} CFA | {note}{promo}{stock}"
            urgency = _urgency_block(card)
            if urgency:
                line += f"\n  {urgency}"
            lines.append(line)

        # Closing sur le #1
        best = cards[0]
        lines.append(
            f"\n🏆 Mon coup de cœur : **{best.name}** — {best.rating_avg}/5, "
            f"c'est le meilleur de la liste. {_closing_line(best)}"
        )

        return "🌟 Voici les mieux notés par nos clients :\n" + "\n".join(lines), cards
    except Exception as exc:
        logger.warning("tool_get_top_rated_closing: %s", exc)
        return "Impossible de récupérer les produits.", []


# ── Tool : get_product_status (closing enrichi) ───────────────

async def tool_get_product_status_closing(
    product_id: Optional[int] = None, product_name: str = "", **_
) -> tuple[str, List["ProductCard"]]:
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            if product_id:
                r = await c.get(f"{DRF_API_BASE}/product/{product_id}/")
            else:
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": product_name})
            r.raise_for_status()
            raw = r.json()

        p = raw if product_id else (
            (raw if isinstance(raw, list) else raw.get("results", []) or [{}])[0]
        )
        if not p:
            return "Produit introuvable. Vérifie le nom ou l'identifiant.", []

        card = _build_product_card(p)
        parts = [f"📦 **{card.name}** — {card.price} CFA"]
        parts.append("✅ En stock" if card.in_stock else "❌ Épuisé — indisponible actuellement")

        if card.has_promo:
            ends = f" (jusqu'au {card.promo_ends_at})" if card.promo_ends_at else ""
            parts.append(
                f"🏷️ Promotion active : -{card.promo_percent}% "
                f"→ **{int(card.promo_price or 0)} CFA**{ends}"
            )
            urgency = _promo_urgency(card)
            if urgency:
                parts.append(urgency)
        else:
            parts.append("Aucune promotion en cours.")

        rating_sig = _rating_signal(card)
        if rating_sig:
            parts.append(rating_sig)


        # Description complète
        if card.description:
            parts.append(f"\n📝 **Description** : {card.description}")

        # Catégorie
        if card.category_name:
            parts.append(f"🏷️ **Catégorie** : {card.category_name}")

        if card.has_active_ad:
            parts.append("📢 Produit mis en avant — très demandé en ce moment.")

        # Closing
        if card.in_stock:
            parts.append(f"\n{_closing_line(card)}")

        return "\n".join(parts), [card]
    except Exception as exc:
        logger.warning("tool_get_product_status_closing: %s", exc)
        return "Je n'ai pas pu récupérer le statut de ce produit.", []


# ── Tool : compare_products (closing enrichi) ─────────────────

async def tool_compare_products_closing(
    product_ids: Optional[List[int]] = None,
    product_names: Optional[List[str]] = None,
    **_,
) -> tuple[str, List["ProductCard"]]:
    import asyncio

    async def _fetch_one(cid: Optional[int], name: str) -> Optional[dict]:
        try:
            async with httpx.AsyncClient(timeout=8) as c:
                if cid:
                    r = await c.get(f"{DRF_API_BASE}/product/{cid}/")
                    r.raise_for_status()
                    return r.json()
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": name})
                r.raise_for_status()
                raw = r.json()
                lst = raw if isinstance(raw, list) else raw.get("results", [])
                return lst[0] if lst else None
        except Exception:
            return None

    ids = product_ids or []
    names = product_names or []
    pairs = [
        (ids[i] if i < len(ids) else None,
         names[i] if i < len(names) else "")
        for i in range(max(len(ids), len(names)))
    ]
    results = await asyncio.gather(*[_fetch_one(cid, nm) for cid, nm in pairs])
    products = [p for p in results if p]

    if not products:
        return "Je n'ai pas trouvé les produits à comparer. Précise les noms ou IDs.", []

    cards = [_build_product_card(p) for p in products]
    lines = ["📊 **Comparaison de produits** :\n"]

    for card in cards:
        note = f"⭐ {card.rating_avg}/5 ({card.rating_count} avis)"
        promo = (f"🏷️ -{card.promo_percent}% → {int(card.promo_price or 0)} CFA"
                 if card.has_promo else "Aucune promo")
        stock = "✅ En stock" if card.in_stock else "❌ Épuisé"
        urgency = _urgency_block(card)
        block = (
            f"**{card.name}**\n"
            f"  Prix    : {card.price} CFA | {promo}\n"
            f"  Note    : {note}\n"
            f"  Stock   : {stock}\n"
            + (f"  Boutique : {card.shop_name}\n" if card.shop_name else "")
            + (f"  _{card.short_description}_\n" if card.short_description else "")
            + (f"  {urgency}\n" if urgency else "")
        )
        lines.append(block)

    # Score composite pour le verdict closing
    def _score(c: "ProductCard") -> float:
        score = c.rating_avg * 2
        if c.has_promo:
            score += 2
        if c.in_stock:
            score += 1
        # Pénalité épuisé
        if not c.in_stock:
            score -= 5
        return score

    available = [c for c in cards if c.in_stock]
    best = max(available or cards, key=_score)

    # Verdict franc
    reasons = []
    if best.has_promo:
        reasons.append(f"il est en promo à -{best.promo_percent}%")
    if best.rating_avg >= 4.0:
        reasons.append(f"noté {best.rating_avg}/5 par les clients")
    if not reasons:
        reasons.append("meilleur rapport qualité/prix")

    lines.append(
        f"🏆 **Mon verdict franc** : prends **{best.name}** — "
        f"{', '.join(reasons)}. Franchement, tu vas pas regretter 💯\n"
        f"{_closing_line(best)}"
    )

    return "\n".join(lines), cards


# ── Tool : get_product_price (closing enrichi) ────────────────

async def tool_get_price_closing(
    product_name: str = "", product_id: Optional[int] = None, **_
) -> tuple[str, List["ProductCard"]]:
    try:
        async with httpx.AsyncClient(timeout=8) as c:
            if product_id:
                r = await c.get(f"{DRF_API_BASE}/product/{product_id}/")
                r.raise_for_status()
                p = r.json()
            else:
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": product_name})
                r.raise_for_status()
                raw = r.json()
                lst = raw if isinstance(raw, list) else raw.get("results", [])
                p = lst[0] if lst else None
        if not p:
            return "Produit introuvable. Vérifie le nom ou l'identifiant.", []

        card = _build_product_card(p)

        if card.has_promo and card.promo_price:
            price_info = (
                f"Le prix de **{card.name}** est de ~~{card.price} CFA~~ "
                f"→ **{int(card.promo_price)} CFA** grâce à la promo 🏷️"
            )
        else:
            price_info = f"Le prix de **{card.name}** est de **{card.price} CFA** 💵"

        urgency = _urgency_block(card)
        result = price_info
        if urgency:
            result += f"\n{urgency}"
        if card.in_stock:
            result += f"\n{_closing_line(card)}"

        return result, [card]
    except Exception as exc:
        logger.warning("tool_get_price_closing: %s", exc)
        return "Je n'ai pas pu récupérer le prix.", []


# ── Tool : suggest_products_for_goal (closing enrichi) ────────

async def tool_suggest_for_goal_closing(
    goal: str = "", keywords: Optional[List[str]] = None, **_
) -> tuple[str, List["ProductCard"]]:
    import asyncio

    if not goal and not keywords:
        return "Décris-moi ton objectif et je trouve les produits pour toi !", []

    search_terms = keywords or [goal]

    async def _search(term: str) -> List[dict]:
        try:
            async with httpx.AsyncClient(timeout=8) as c:
                r = await c.get(f"{DRF_API_BASE}/product/search_products/",
                                params={"q": term})
                r.raise_for_status()
                raw = r.json()
                lst = raw if isinstance(raw, list) else raw.get("results", [])
                return lst[:2]
        except Exception:
            return []

    all_results = await asyncio.gather(*[_search(t) for t in search_terms])

    seen: set = set()
    products: List[dict] = []
    for batch in all_results:
        for p in batch:
            if p.get("id") not in seen:
                seen.add(p["id"])
                products.append(p)

    if not products:
        return (
            f"Je n'ai pas encore de produits pour « {goal} » sur la plateforme. "
            f"Nos vendeurs enrichissent le catalogue chaque jour ! 🌍",
            [],
        )

    cards = [_build_product_card(p) for p in products]
    intro = f"Pour **{goal}**, voici ce que je te propose 🎯 :\n"
    lines = []
    for card in cards:
        line = (
            f"• **{card.name}** — {card.price} CFA"
            + (f" 🏷️ -{card.promo_percent}%" if card.has_promo else "")
            + ("" if card.in_stock else " *(épuisé)*")
        )
        urgency = _urgency_block(card)
        if urgency:
            line += f"\n  {urgency}"
        lines.append(line)

    # Meilleure sélection pour le closing
    available = [c for c in cards if c.in_stock]
    if available:
        top = max(available, key=lambda c: c.rating_avg)
        lines.append(
            f"\n💡 Mon conseil : commence par **{top.name}** — "
            f"c'est le coup de cœur du moment pour cet objectif 👌\n"
            f"{_closing_line(top)}"
        )

    return intro + "\n".join(lines), cards


# ═════════════════════════════════════════════════════════════
# Mise à jour du TOOL_REGISTRY avec les versions closing
# ═════════════════════════════════════════════════════════════

TOOL_REGISTRY.update({
    "search_products":           tool_search_products_closing,
    "get_top_rated_products":    tool_get_top_rated_closing,
    "get_product_status":        tool_get_product_status_closing,
    "compare_products":          tool_compare_products_closing,
    "suggest_products_for_goal": tool_suggest_for_goal_closing,
    "get_product_price":         tool_get_price_closing,
    "get_new_and_promos":        tool_get_new_and_promos,
    # track_order et none restent inchangés
})