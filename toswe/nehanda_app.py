# nehanda_app.py
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, List

# --- FastAPI / Pydantic ---
from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Cookie

# --- SQLAlchemy (db des conversations, distincte de Django) ---
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

# --- Django ORM (pour CustomUser & settings) ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "toswe.settings"))
import django  # type: ignore
django.setup()
from django.conf import settings
from users.models import CustomUser  # ton modèle CustomUser existant côté Django

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# ============ SQLAlchemy setup (DB conversations) ============
CONV_DB_URL = os.getenv("CONVERSATIONS_DB_URL", "sqlite:///./conversations.db")
engine = create_engine(CONV_DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "user" | "nehanda"
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

Base.metadata.create_all(bind=engine)

# ============ FastAPI schemas ============
class ChatIn(BaseModel):
    message: str
    conversation_id: Optional[int] = None  # si non fourni, on (re)prend la conv active ou on crée

class ChatOut(BaseModel):
    conversation_id: int
    response: str

class MessageOut(BaseModel):
    id: int
    sender: str
    text: str
    created_at: datetime

class ConversationOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    messages: List[MessageOut]

# ============ Dependencies ============
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Cookie(None)
) -> CustomUser:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    elif access_token:
        token = access_token
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    phone = payload.get("phone")
    if not phone:
        raise HTTPException(status_code=401, detail="Invalid payload")

    try:
        user = CustomUser.objects.get(phone=phone)
    except CustomUser.DoesNotExist:
        raise HTTPException(status_code=401, detail="CustomUser not found")
    return user

import re
import httpx
import spacy
from typing import Optional

# --- NLP (juste pour entités de spaCy) ---
import spacy
import httpx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Charger le modèle SpaCy français
nlp = spacy.load("fr_core_news_sm")

# --- API DRF ---
DRF_API_BASE = "http://127.0.0.1:8000/api"

# --- Intent keywords (règles) ---
# --- Intents (mots-clés associés aux intentions) ---
RULE_INTENTS = {
    # Général / meta
    "who_created": ["qui a créé", "créateur", "qui vous a créé", "qui est derrière", "créateurs", "créatrice"],
    "what_is_nehanda": ["qui es-tu", "qui es tu", "nehanda", "qui es nehanda", "présente-toi", "présente toi"],
    "what_is_toswe": ["toswe", "tôswè", "comment ça marche", "comment fonctionne", "qu'est-ce que toswé", "c'est quoi toswè", "c'est quoi to swe"],

    # Produits / catalogue
    "search_product": ["cherche", "montre-moi", "trouve", "produit", "article", "que avez-vous", "quels produits", "rechercher"],
    "get_price": ["prix", "combien coûte", "coûte", "tarif", "combien"],
    "check_availability": ["en stock", "disponible", "disponibilité", "disponibles", "est-ce disponible"],
    "promo_info": ["promo", "promotion", "réduction", "soldes", "bon plan", "bons plans"],
    "sponsor_info": ["sponsoris", "sponsorisé", "sponsoriser", "mise en avant", "mettre en avant"],

    # Commandes
    "place_order": ["comment passer une commande", "comment commander", "passer la commande", "je veux commander", "comment j'achète", "commander"],
    "track_order": ["suivi", "où est ma commande", "où est la commande", "numéro de commande", "suivre ma commande", "statut de ma commande"],
    "cancel_order": ["annuler", "annulation", "supprimer ma commande", "je veux annuler"],
    "modify_order": ["modifier la commande", "modifier ma commande", "changer la commande", "changer ma commande"],

    # Livraison
    "delivery_fees": ["frais de livraison", "prix livraison", "coût livraison", "frais"],
    "delivery_time": ["délai de livraison", "quand livré", "livré quand", "combien de temps pour la livraison"],
    "delivery_modes": ["mode de livraison", "comment livré", "livraison à domicile", "retrait"],
    "check_zone_delivery": ["livrez", "livrez à", "livraison à", "couvrez", "porto-novo", "cotonou", "abomey"],
    "delivery_person": ["qui va livrer", "quel livreur", "qui est chargé de la livraison"],

    # Paiement
    "payment_modes": ["mode de paiement", "moyens de paiement", "paiement"],
    "payment_mobile_money": ["mobile money", "momo", "mtn", "moov"],
    "payment_cash_on_delivery": ["paiement à la livraison", "paiement à la réception", "cash à la livraison"],
    "payment_failed": ["paiement échoué", "paiement a échoué", "erreur paiement"],

    # Vendeurs / boutiques
    "become_seller": ["devenir vendeur", "comment devenir vendeur", "vendre sur", "ouvrir une boutique", "inscrire comme vendeur"],
    "local_brands": ["marque locale", "marques locales", "marques africaines"],
    "popular_shops": ["boutiques populaires", "shops populaires", "magasins populaires"],
    "find_shop": ["où trouver", "quelle boutique vend", "quelle boutique"],

    # Promotion & sponsorisation
    "sponsor_product": ["sponsoriser mon produit", "sponsoriser", "sponsorisation"],
    "promo_vs_sponsor": ["différence promo sponsor", "promo vs sponsor", "quelle est la différence entre promo et sponsor"],

    # Compte & support
    "create_account": ["créer un compte", "inscrire", "s'inscrire", "je veux m'inscrire"],
    "reset_password": ["mot de passe oublié", "réinitialiser mot de passe", "reset password"],
    "contact_support": ["contact", "support", "aide", "contacter le support", "whatsapp", "assistance"],

    # Recommandation & nouveautés
    "new_products": ["nouveautés", "nouveaux produits", "arrivage"],
    "recommend_products": ["recommande", "conseilles", "je cherche une suggestion", "quel produit me conseille"],

    # Divers
    "product_variants": ["taille", "couleur", "variantes", "variantes du produit"],
    "product_usage": ["comment utiliser", "mode d'emploi", "utiliser ce produit", "instruction"],
    "product_compatibility": ["compatible", "compatibilité"],
    "popular_products": ["les plus vendus", "best-seller", "plus vendus"],
    "budget_recommendation": ["budget", "je veux quelque chose pour", "mon budget"],
}

# --- Réponses statiques (alignées avec les intents) ---
STATIC_RESPONSES = {
    # Général / meta
    "who_created": [
        "Je suis Nehanda, née dans le laboratoire Tôswè 💡 — créée par une équipe d’ingénieurs passionnés.",
        "Derrière moi, il y a l’équipe Tôswè, des humains brillants qui m’entraînent chaque jour 🌍.",
        "Mes créateurs ? Une belle équipe de Tôswè qui croit en l’innovation locale ✨.",
    ],
    "what_is_nehanda": [
        "Je suis Nehanda, ton assistante virtuelle Tôswè 🤖. Je peux t’aider à trouver des produits, commander et obtenir du support.",
        "On m’appelle Nehanda, je suis l’IA de Tôswè — mon rôle est de te guider dans tes achats 🛍️.",
        "Moi, c’est Nehanda ! L’assistante digitale qui rend Tôswè plus simple, plus rapide et plus fun 😎.",
    ],
    "what_is_toswe": [
        "Tôswè est une plateforme qui connecte clients et vendeurs 🛒.",
        "Avec Tôswè, tu découvres produits, promos et boutiques locales 🌍.",
        "Tôswè, c’est ton marché digital simple, rapide et sécurisé ✨.",
    ],

    # Produits / catalogue
    "search_product": [
        "Tu peux explorer nos différentes catégories pour découvrir les produits 📂.",
        "Il y a des milliers de produits dans le catalogue Tôswè 📦.",
    ],
    "get_price": [
        "Le prix est actuellement de ... 💵.",
        "Ce produit coûte ... CFA 💳.",
    ],
    "check_availability": [
        "Ce produit est disponible ✅.",
        "Désolé, ce produit est en rupture pour le moment ❌.",
    ],
    "promo_info": [
        "Voici les promos en cours 🔥 : ...",
        "Actuellement, tu peux profiter de réductions sur certains articles 🏷️.",
    ],
    "sponsor_info": [
        "Ces produits sont sponsorisés : ...",
        "Voici la liste des articles mis en avant par nos vendeurs 💡.",
    ],

    # Commandes
    "place_order": [
        "Pour commander, choisis ton produit et clique sur 'Acheter' 🛍️.",
        "Passe ta commande en quelques clics simples 💡.",
    ],
    "track_order": [
        "Tu peux suivre ta commande directement dans l’app 📱.",
        "Entre ton numéro de commande et je te donne l’état 📦.",
    ],
    "cancel_order": [
        "Tu peux annuler ta commande depuis ton historique 📋.",
        "Contacte le support si tu souhaites l’annuler après validation.",
    ],
    "modify_order": [
        "Tu peux modifier ta commande tant qu’elle n’est pas expédiée ✍️.",
        "Après expédition, contacte le support pour changer ta commande.",
    ],

    # Livraison
    "delivery_fees": [
        "Les frais de livraison varient entre 500 et 2000 CFA 💰.",
        "Ça dépend de la zone, mais c’est toujours abordable 😉.",
    ],
    "delivery_time": [
        "La livraison prend entre 24h et 72h selon ta localisation ⏳.",
        "En général, tes articles arrivent rapidement 🚚.",
    ],
    "delivery_modes": [
        "Livraison standard ou express 🚀.",
        "Tu peux choisir le mode de livraison adapté 💡.",
    ],
    "check_zone_delivery": [
        "Nous livrons partout au Bénin 🇧🇯.",
        "Tôswè couvre toutes les grandes villes 📦.",
    ],
    "delivery_person": [
        "Un livreur partenaire viendra jusqu’à toi 🚴.",
        "Nos livreurs de confiance assurent la livraison 📦.",
    ],

    # Paiement
    "payment_modes": [
        "Nous acceptons mobile money, cash à la livraison et carte bancaire 💳.",
        "Tu as plusieurs choix de paiement pratiques 😉.",
    ],
    "payment_mobile_money": [
        "Oui, tu peux payer avec MTN MoMo ou Moov Money 📲.",
        "Le mobile money est accepté, rapide et sécurisé 🔐.",
    ],
    "payment_cash_on_delivery": [
        "Oui, tu peux payer cash à la livraison 💵.",
        "Paiement à la livraison disponible ✅.",
    ],
    "payment_failed": [
        "Désolé 😔, il semble y avoir un souci. Réessaie ou contacte le support.",
        "Si ton paiement a échoué, vérifie ton solde ou contacte ton opérateur 📞.",
    ],

    # Vendeurs / boutiques
    "become_seller": [
        "Pour devenir vendeur, inscris-toi et active ton compte vendeur 🏪.",
        "Tu peux créer ta boutique facilement depuis l’app ✨.",
    ],
    "local_brands": [
        "Nous mettons en avant les marques locales 🇧🇯.",
        "Découvre les produits made in Bénin 🌍.",
    ],
    "popular_shops": [
        "Ces boutiques sont très populaires sur Tôswè 📈 : ...",
        "Les vendeurs les plus appréciés sont : ...",
    ],
    "find_shop": [
        "La boutique la mieux notée pour ce produit est ... ⭐.",
        "Ce vendeur propose le meilleur rapport qualité-prix 👌.",
    ],

    # Promotion & sponsorisation
    "sponsor_product": [
        "Oui, tu peux sponsoriser tes produits pour plus de visibilité 📢.",
        "Les articles sponsorisés apparaissent en haut des résultats 🚀.",
    ],
    "promo_vs_sponsor": [
        "Une promo baisse le prix 💵, un sponsor met ton produit en avant 📢.",
        "La promo attire par le prix, la sponsorisation par la visibilité 🌍.",
    ],

    # Compte & support
    "create_account": [
        "Pour t’inscrire, clique sur 'Créer un compte' 🔑.",
        "Crée ton compte en quelques étapes simples 📱.",
    ],
    "reset_password": [
        "Clique sur 'Mot de passe oublié' pour réinitialiser 🔐.",
        "Pas de panique 😅, tu peux récupérer ton compte facilement.",
    ],
    "contact_support": [
        "Tu peux contacter le support via l’app ou au +229 90 00 00 00 📞.",
        "L’assistance Tôswè est là pour toi 24/7 🤝.",
    ],

    # Recommandation & nouveautés
    "new_products": [
        "Voici les nouveautés sur Tôswè 🆕 : ...",
        "Les derniers produits ajoutés sont : ...",
    ],
    "recommend_products": [
        "Je te recommande ces articles selon tes goûts 🎯.",
        "Tu pourrais aimer : ...",
    ],

    # Divers
    "product_variants": [
        "Ce produit existe en plusieurs tailles et couleurs 🎨.",
        "Choisis la variante qui te convient 👌.",
    ],
    "product_usage": [
        "Tu trouveras les instructions d’utilisation dans la fiche produit 📖.",
        "Voici comment utiliser ce produit : ...",
    ],
    "product_compatibility": [
        "Ce produit est compatible avec ... 🔌.",
        "Vérifie bien la compatibilité avant achat ⚠️.",
    ],
    "popular_products": [
        "Les best-sellers de la semaine sont 📈 : ...",
        "Voici les articles les plus vendus : ...",
    ],
    "budget_recommendation": [
        "Avec ton budget, je te propose ces articles 💡.",
        "Voici les meilleures options dans ta gamme de prix 💵.",
    ],
}


import random
from typing import Optional

# --- Matching rules ---
def match_rule_intent(text: str):
    """
    Renvoie l'intent si une règle match (priorise expressions longues, puis mots).
    """
    text_lower = text.lower()
    doc = nlp(text_lower)

    tokens = {t.text.lower() for t in doc if not t.is_punct and not t.is_space}
    tokens |= {t.lemma_.lower() for t in doc if not t.is_punct and not t.is_space}

    # 1) Expressions exactes (priorité aux mots composés)
    for intent, kws in RULE_INTENTS.items():
        for kw in kws:
            if " " in kw and kw.lower() in text_lower:
                return intent

    # 2) Tokens ou sous-chaînes
    for intent, kws in RULE_INTENTS.items():
        for kw in kws:
            kw_l = kw.lower()
            if kw_l in tokens or (" " not in kw_l and kw_l in text_lower):
                return intent

    return None


# --- Extraction d'entités ---
def extract_entities(doc, text: str):
    entities = {"PRODUCT": [], "LOCATION": [], "ORDER_ID": [], "ORG": []}

    for ent in doc.ents:
        if ent.label_ in ["LOC", "GPE"]:  # Localisation
            entities["LOCATION"].append(ent.text)
        elif ent.label_ in ["PRODUCT", "MISC"]:
            entities["PRODUCT"].append(ent.text)
        elif ent.label_ in ["ORG"]:
            entities["ORG"].append(ent.text)

    # Détection manuelle d'ID commande
    import re
    match = re.findall(r"#\d+", text)
    if match:
        entities["ORDER_ID"].extend(match)

    return entities


def detect_intent_and_entities(text: str):
    """
    Détection hybride : règles (match_rule_intent) + entités NLP
    Retourne (intent, source, entities)
    """
    text_lower = text.lower()
    doc = nlp(text_lower)

    # 1) Règles
    intent = match_rule_intent(text)
    if intent:
        return intent, "rule", extract_entities(doc, text)

    # 2) Rien trouvé
    return None, "none", extract_entities(doc, text)


# --- Réponse Nehanda ---
async def nehanda_brain_reply(user, message: str, token: Optional[str] = None) -> str:
    intent, source, entities = detect_intent_and_entities(message)

    print(f"[DEBUG] Intent détecté: {intent} | Source: {source} | Entities: {entities}")

    # Si on a une réponse statique connue → choisir une au hasard
    if intent in STATIC_RESPONSES:
        responses = STATIC_RESPONSES[intent]
        return random.choice(responses)

    # Cas fallback : pas d’intent reconnu
    return (
        f"Je ne suis pas encore assez intelligente pour répondre précisément à ton message 😊. "
        f"Mes créateurs y travaillent — en attendant, contacte le support (+229 90 00 00 00) et je ferai de mon mieux pour t'aider."
    )




# ============ FastAPI app ============
app = FastAPI(title="Nehanda", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],  #  frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Response

@app.post("/refresh_token")
def refresh_token(
    refresh_token: Optional[str] = Cookie(None),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh")

    phone = payload.get("phone")
    if not phone:
        raise HTTPException(status_code=401, detail="Invalid payload")

    # Vérifier user
    try:
        user = CustomUser.objects.get(phone=phone)
    except CustomUser.DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found")

    # Générer nouveau access_token
    new_access = jwt.encode(
        {"phone": user.phone, "exp": datetime.utcnow() + timedelta(minutes=5)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return {"access": new_access}



from fastapi import Depends
from fastapi.concurrency import run_in_threadpool

@app.post("/nehanda/chat", response_model=ChatOut)
async def chat_with_nehanda(
    payload: ChatIn,
    db: Session = Depends(get_db),
    user: CustomUser = Depends(get_current_user),
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Cookie(None)
):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    elif access_token:
        token = access_token

    # 1) Conversation
    conv: Optional[Conversation] = None
    if payload.conversation_id:
        conv = db.get(Conversation, payload.conversation_id)
        if not conv or conv.user_id != user.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = db.query(Conversation).filter(Conversation.user_id == user.id).order_by(Conversation.id.desc()).first()
        if conv is None:
            conv = Conversation(user_id=user.id)
            db.add(conv)
            db.flush()

    # 2) Message utilisateur
    db.add(Message(conversation_id=conv.id, sender=user.username, text=payload.message))

    # 3) Réponse Nehanda (async)
    reply = await nehanda_brain_reply(user, payload.message, token)

    # 4) Sauvegarde
    db.add(Message(conversation_id=conv.id, sender="nehanda", text=reply))
    db.commit()

    return ChatOut(conversation_id=conv.id, response=reply)


@app.get("/conversations/{conversation_id}", response_model=ConversationOut)
def get_conversation(conversation_id: int, db: Session = Depends(get_db), user: CustomUser = Depends(get_current_user)):
    conv = db.get(Conversation, conversation_id)
    if not conv or conv.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Charger messages pour la réponse Pydantic
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.id.asc())
        .all()
    )

    return ConversationOut(
        id=conv.id,
        user_id=conv.user_id,
        created_at=conv.created_at,
        messages=[MessageOut(id=m.id, sender=m.sender, text=m.text, created_at=m.created_at) for m in msgs],
    )


