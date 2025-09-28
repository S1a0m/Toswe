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
nlp = spacy.blank("fr")

# --- API DRF ---
DRF_API_BASE = "http://127.0.0.1:8000/api"

# --- Intent keywords (règles) ---
RULE_INTENTS = {
    "payment_info": ["paiement", "espèces", "mobile money"],
    "support_request": ["aide", "support", "problème", "bug", "contact"],
    "track_order": ["commande", "suivi", "livraison"],
}

# --- ML: classification des intentions ---
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TRAIN_DATA = [
    # -------------------------
    # Produits & Catalogue
    # -------------------------
    ("Quels produits sont disponibles dans la catégorie X ?", "search_product"),
    ("Montre-moi ce que vous avez dans la catégorie X.", "search_product"),
    ("Je cherche les articles de la catégorie X.", "search_product"),
    ("Quels articles proposez-vous dans X ?", "search_product"),
    ("Quels produits peut-on trouver dans la section X ?", "search_product"),

    ("Montre-moi les promos du moment.", "promo_info"),
    ("Quels articles sont en promotion ?", "promo_info"),
    ("Y a-t-il des réductions disponibles ?", "promo_info"),
    ("Quels sont vos bons plans ?", "promo_info"),
    ("Quelles sont les offres spéciales en cours ?", "promo_info"),

    ("Quels sont les produits sponsorisés ?", "sponsor_info"),
    ("Peux-tu me montrer les articles sponsorisés ?", "sponsor_info"),
    ("Quels produits sont mis en avant ?", "sponsor_info"),
    ("Qu’est-ce qui est sponsorisé actuellement ?", "sponsor_info"),
    ("Quels articles bénéficient d’une mise en avant ?", "sponsor_info"),

    ("Ce produit est-il en stock ?", "check_availability"),
    ("Est-ce que le produit X est disponible ?", "check_availability"),
    ("Vous avez encore du stock pour X ?", "check_availability"),
    ("Puis-je commander X en ce moment ?", "check_availability"),
    ("Le produit X est encore en vente ?", "check_availability"),

    ("Quel est le prix de X ?", "get_price"),
    ("Combien coûte le produit X ?", "get_price"),
    ("Peux-tu me donner le prix de X ?", "get_price"),
    ("C’est combien pour X ?", "get_price"),
    ("Le tarif de X c’est combien ?", "get_price"),

    ("Quelle boutique vend X au meilleur prix ?", "best_shop"),
    ("Où puis-je trouver X au prix le plus bas ?", "best_shop"),
    ("Qui vend X le moins cher ?", "best_shop"),
    ("Quelle boutique fait la meilleure offre pour X ?", "best_shop"),
    ("Quel vendeur propose X au meilleur tarif ?", "best_shop"),

    ("Donne-moi des alternatives à ce produit.", "get_alternatives"),
    ("Quels produits similaires à X proposez-vous ?", "get_alternatives"),
    ("Tu peux me montrer d’autres choix comme X ?", "get_alternatives"),
    ("Y a-t-il des options alternatives à X ?", "get_alternatives"),
    ("Quels autres articles équivalents à X avez-vous ?", "get_alternatives"),

    # -------------------------
    # Commandes
    # -------------------------
    ("Comment passer une commande ?", "place_order"),
    ("Comment j’achète un produit sur Tôswè ?", "place_order"),
    ("Explique-moi comment commander.", "place_order"),
    ("Quelles sont les étapes pour passer commande ?", "place_order"),
    ("Je veux commander, comment ça marche ?", "place_order"),

    ("Où en est ma commande #123 ?", "track_order"),
    ("Peux-tu me donner le suivi de la commande #123 ?", "track_order"),
    ("Ma commande #123 est où ?", "track_order"),
    ("Quel est l’état actuel de ma commande #123 ?", "track_order"),
    ("Où se trouve ma commande #123 actuellement ?", "track_order"),

    ("Est-ce que je peux modifier ma commande ?", "modify_order"),
    ("Puis-je changer ma commande après l’avoir faite ?", "modify_order"),
    ("Comment éditer une commande déjà passée ?", "modify_order"),
    ("Je veux modifier ma commande, c’est possible ?", "modify_order"),
    ("Peut-on mettre à jour une commande existante ?", "modify_order"),

    ("Quels sont les frais de livraison ?", "delivery_fees"),
    ("Combien coûte la livraison ?", "delivery_fees"),
    ("Les frais de livraison sont de combien ?", "delivery_fees"),
    ("Peux-tu me dire le prix de la livraison ?", "delivery_fees"),
    ("Quel est le tarif pour la livraison ?", "delivery_fees"),

    ("Puis-je annuler une commande ?", "cancel_order"),
    ("Comment annuler ma commande ?", "cancel_order"),
    ("Je veux annuler ma commande, comment faire ?", "cancel_order"),
    ("Est-ce possible de supprimer ma commande ?", "cancel_order"),
    ("Je voudrais annuler une commande déjà faite.", "cancel_order"),

    # -------------------------
    # Livraison
    # -------------------------
    ("Quand est-ce que ma commande sera livrée ?", "delivery_time"),
    ("Quel est le délai de livraison ?", "delivery_time"),
    ("Combien de temps faut-il pour recevoir ma commande ?", "delivery_time"),
    ("Ma livraison arrive quand ?", "delivery_time"),
    ("En combien de jours la commande arrive ?", "delivery_time"),

    ("Quels sont les modes de livraison disponibles ?", "delivery_modes"),
    ("Comment puis-je être livré ?", "delivery_modes"),
    ("Quels types de livraison proposez-vous ?", "delivery_modes"),
    ("Vous livrez comment ?", "delivery_modes"),
    ("Quels choix de livraison sont possibles ?", "delivery_modes"),

    ("Puis-je être livré à Porto-Novo ?", "check_zone_delivery"),
    ("Est-ce que vous livrez à Porto-Novo ?", "check_zone_delivery"),
    ("La livraison est-elle possible à Porto-Novo ?", "check_zone_delivery"),
    ("Livrez-vous dans ma ville Porto-Novo ?", "check_zone_delivery"),
    ("Je veux savoir si vous couvrez Porto-Novo.", "check_zone_delivery"),

    ("Qui va livrer mon colis ?", "delivery_person"),
    ("Quel livreur prendra ma commande ?", "delivery_person"),
    ("Qui est chargé de la livraison ?", "delivery_person"),
    ("C’est quel livreur qui s’occupe de mon colis ?", "delivery_person"),
    ("Quel partenaire livreur me livre ?", "delivery_person"),

    # -------------------------
    # Paiement
    # -------------------------
    ("Quels sont les modes de paiement disponibles ?", "payment_modes"),
    ("Comment puis-je payer ma commande ?", "payment_modes"),
    ("Quels moyens de paiement acceptez-vous ?", "payment_modes"),
    ("Je peux payer avec quoi ?", "payment_modes"),
    ("Quelles options de paiement proposez-vous ?", "payment_modes"),

    ("Est-ce que vous acceptez Mobile Money ?", "payment_mobile_money"),
    ("Puis-je payer via Mobile Money ?", "payment_mobile_money"),
    ("Le paiement mobile est accepté ?", "payment_mobile_money"),
    ("Je peux payer avec MoMo ?", "payment_mobile_money"),
    ("Mobile Money est disponible comme moyen de paiement ?", "payment_mobile_money"),

    ("Puis-je payer à la livraison ?", "payment_cash_on_delivery"),
    ("Est-ce que le paiement à la livraison est possible ?", "payment_cash_on_delivery"),
    ("Puis-je régler en cash à la livraison ?", "payment_cash_on_delivery"),
    ("Vous acceptez paiement à la réception ?", "payment_cash_on_delivery"),
    ("Je peux payer quand le colis arrive ?", "payment_cash_on_delivery"),

    ("Mon paiement a échoué, que faire ?", "payment_failed"),
    ("Pourquoi mon paiement n’est pas passé ?", "payment_failed"),
    ("J’ai un problème avec mon paiement.", "payment_failed"),
    ("Le paiement a échoué, comment résoudre ça ?", "payment_failed"),
    ("Mon règlement n’a pas marché, que dois-je faire ?", "payment_failed"),

    # -------------------------
    # Boutiques & Vendeurs
    # -------------------------
    ("Quelles sont les boutiques populaires ?", "popular_shops"),
    ("Montre-moi les boutiques les plus connues.", "popular_shops"),
    ("Quels magasins sont tendances ?", "popular_shops"),
    ("Quelles sont les enseignes les plus visitées ?", "popular_shops"),
    ("Quels sont les shops préférés des clients ?", "popular_shops"),

    ("Quels vendeurs vendent dans la catégorie X ?", "sellers_by_category"),
    ("Qui propose des produits dans X ?", "sellers_by_category"),
    ("Quels marchands vendent dans X ?", "sellers_by_category"),
    ("Quels sont les vendeurs de la section X ?", "sellers_by_category"),
    ("Peux-tu me lister les vendeurs de la catégorie X ?", "sellers_by_category"),

    ("Quelles marques locales sont disponibles ?", "local_brands"),
    ("Quels sont vos partenaires locaux ?", "local_brands"),
    ("Montre-moi les marques du pays.", "local_brands"),
    ("Quelles marques africaines proposez-vous ?", "local_brands"),
    ("Quels labels locaux sont disponibles ?", "local_brands"),

    ("Comment devenir vendeur sur Tôswè ?", "become_seller"),
    ("Je veux vendre sur Tôswè, comment faire ?", "become_seller"),
    ("Quelles sont les conditions pour être vendeur ?", "become_seller"),
    ("Comment ouvrir une boutique sur Tôswè ?", "become_seller"),
    ("Je souhaite m’inscrire comme vendeur, comment procéder ?", "become_seller"),

    # -------------------------
    # Promotion & Sponsorisation
    # -------------------------
    ("Quels sont les produits en promotion ?", "promo_info"),
    ("Quelles promos sont actives ?", "promo_info"),
    ("Quels articles sont soldés ?", "promo_info"),
    ("Quels sont les rabais en cours ?", "promo_info"),

    ("Comment sponsoriser mon produit ?", "sponsor_product"),
    ("Que faut-il faire pour sponsoriser un article ?", "sponsor_product"),
    ("Je veux mettre en avant mon produit, comment ?", "sponsor_product"),
    ("Comment rendre mon produit sponsorisé ?", "sponsor_product"),

    ("Quelle est la différence entre promo et sponsorisation ?", "promo_vs_sponsor"),
    ("Promo et sponsor, c’est quoi la différence ?", "promo_vs_sponsor"),
    ("Explique-moi promo vs sponsorisation.", "promo_vs_sponsor"),
    ("Quelle est la distinction entre promotion et sponsorisation ?", "promo_vs_sponsor"),

    # -------------------------
    # Compte & Support
    # -------------------------
    ("Comment créer un compte ?", "create_account"),
    ("Je veux m’inscrire, comment faire ?", "create_account"),
    ("Quelles sont les étapes pour ouvrir un compte ?", "create_account"),
    ("Peux-tu m’aider à créer un compte ?", "create_account"),

    ("Comment réinitialiser mon mot de passe ?", "reset_password"),
    ("J’ai oublié mon mot de passe, que faire ?", "reset_password"),
    ("Peux-tu m’aider à réinitialiser mon mot de passe ?", "reset_password"),
    ("Je n’arrive pas à me connecter, mot de passe oublié.", "reset_password"),

    ("Comment contacter le support ?", "contact_support"),
    ("J’ai besoin d’aide, comment contacter le service client ?", "contact_support"),
    ("Donnez-moi le contact du support.", "contact_support"),
    ("Comment joindre le SAV ?", "contact_support"),

    # -------------------------
    # Recommandations & Nouveaux produits
    # -------------------------
    ("Quels sont les nouveaux produits ?", "new_products"),
    ("Montre-moi les nouveautés.", "new_products"),
    ("Quels articles viennent d’arriver ?", "new_products"),
    ("Quelles sont vos dernières nouveautés ?", "new_products"),

    ("Peux-tu me recommander des produits dans la catégorie X ?", "recommend_products"),
    ("Quels produits me conseilles-tu dans la catégorie X ?", "recommend_products"),
    ("Tu peux me proposer des articles de X ?", "recommend_products"),
    ("Fais-moi une recommandation dans la catégorie X.", "recommend_products"),

    ("Quels produits sont en promo/sponsorisés ?", "promo_or_sponsor"),
    ("Qu’est-ce qui est en promotion ou sponsorisé ?", "promo_or_sponsor"),
    ("Quels articles bénéficient d’une promo ou d’un sponsor ?", "promo_or_sponsor"),
    ("Montre-moi les promos et sponsors.", "promo_or_sponsor"),

    ("Ce produit existe-t-il dans plusieurs tailles/couleurs ?", "product_variants"),
    ("Y a-t-il différentes tailles ou couleurs pour ce produit ?", "product_variants"),
    ("Ce produit est-il disponible en plusieurs versions ?", "product_variants"),
    ("Je peux choisir des variantes de ce produit ?", "product_variants"),

    # -------------------------
    # Comparaison et Conseils
    # -------------------------
    ("Quel est le meilleur produit pour [besoin particulier] ?", "best_for_need"),
    ("Que me conseilles-tu pour [besoin] ?", "best_for_need"),
    ("Quel produit correspond le mieux à [besoin] ?", "best_for_need"),
    ("Peux-tu recommander le top produit pour [besoin] ?", "best_for_need"),

    ("Quel produit me conseilles-tu entre X et Y ?", "compare_products"),
    ("Lequel est mieux entre X et Y ?", "compare_products"),
    ("Comparons X et Y, lequel choisir ?", "compare_products"),
    ("X vs Y, quel est le meilleur ?", "compare_products"),

    ("Quelle marque est la plus fiable dans [catégorie] ?", "brand_reliability"),
    ("Quelle marque me conseilles-tu dans [catégorie] ?", "brand_reliability"),
    ("Laquelle est la marque la plus sûre dans [catégorie] ?", "brand_reliability"),
    ("Dans [catégorie], quelle marque a la meilleure réputation ?", "brand_reliability"),

    ("Quels sont les produits populaires/les plus vendus ?", "popular_products"),
    ("Quels articles sont les plus achetés ?", "popular_products"),
    ("Peux-tu me montrer les produits tendances ?", "popular_products"),
    ("Qu’est-ce qui se vend le mieux actuellement ?", "popular_products"),

    ("Que puis-je acheter avec un budget de Z ?", "budget_recommendation"),
    ("Quels produits correspondent à un budget de Z ?", "budget_recommendation"),
    ("Propose-moi des articles avec Z comme budget.", "budget_recommendation"),
    ("Avec Z, qu’est-ce que je peux avoir ?", "budget_recommendation"),

    # -------------------------
    # Boutiques
    # -------------------------
    ("Quelle boutique vend le produit X ?", "find_shop"),
    ("Où trouver le produit X ?", "find_shop"),
    ("Quel magasin propose X ?", "find_shop"),
    ("Dans quelle boutique acheter X ?", "find_shop"),

    ("Quelles sont les meilleures boutiques de [catégorie] ?", "best_shops_by_category"),
    ("Quels magasins sont top dans [catégorie] ?", "best_shops_by_category"),
    ("Peux-tu me donner les meilleures boutiques de [catégorie] ?", "best_shops_by_category"),
    ("Quelles enseignes sont recommandées pour [catégorie] ?", "best_shops_by_category"),

    ("Quelle boutique est la plus proche de moi ?", "nearest_shop"),
    ("Quel magasin est le plus proche ?", "nearest_shop"),
    ("Peux-tu m’indiquer la boutique la plus proche ?", "nearest_shop"),
    ("Où est la boutique la plus proche de ma position ?", "nearest_shop"),

    ("Est-ce que le vendeur X est vérifié ?", "seller_verified"),
    ("Le vendeur X est-il de confiance ?", "seller_verified"),
    ("Est-ce que X est un vendeur validé ?", "seller_verified"),
    ("Le vendeur X est-il certifié ?", "seller_verified"),

    # -------------------------
    # Conseils d’usage produits
    # -------------------------
    ("Comment utiliser ce produit ?", "product_usage"),
    ("Donne-moi les instructions pour utiliser ce produit.", "product_usage"),
    ("Peux-tu expliquer l’utilisation de ce produit ?", "product_usage"),
    ("Comment s’emploie ce produit ?", "product_usage"),

    ("Est-ce que ce produit est compatible avec [autre produit] ?", "product_compatibility"),
    ("Ce produit fonctionne-t-il avec [autre produit] ?", "product_compatibility"),
    ("Puis-je utiliser ce produit avec [autre produit] ?", "product_compatibility"),
    ("X et Y sont-ils compatibles ?", "product_compatibility"),

    ("Quelle est la durée de vie de ce produit ?", "product_lifetime"),
    ("Combien de temps dure ce produit ?", "product_lifetime"),
    ("Ce produit est-il durable ?", "product_lifetime"),
    ("Quelle est la longévité de ce produit ?", "product_lifetime"),

    ("Comment entretenir ce produit ?", "product_maintenance"),
    ("Quels sont les conseils d’entretien pour ce produit ?", "product_maintenance"),
    ("Comment garder ce produit en bon état ?", "product_maintenance"),
    ("Peux-tu m’expliquer l’entretien de ce produit ?", "product_maintenance"),
]



X = [x for x, y in TRAIN_DATA]
y = [y for x, y in TRAIN_DATA]

clf = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("logreg", LogisticRegression())
])
clf.fit(X, y)

# --- Helpers API DRF ---
async def fetch_products(query: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{DRF_API_BASE}/product/", params={"search": query})
        return r.json() if r.status_code == 200 else None

async def fetch_order(order_id: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{DRF_API_BASE}/order/{order_id}/", headers=headers)
        return r.json() if r.status_code == 200 else None

async def fetch_promos():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{DRF_API_BASE}/product/", params={"promo": "true"})
        return r.json() if r.status_code == 200 else None

# --- Détection hybride ---
def detect_intent_and_entities(text: str):
    text_lower = text.lower()
    doc = nlp(text_lower)

    # 1) Règles simples
    for intent, keywords in RULE_INTENTS.items():
        if any(word in text_lower for word in keywords):
            return intent, "rule", extract_entities(doc, text)

    # 2) Sinon, fallback ML
    intent = clf.predict([text])[0]
    return intent, "ml", extract_entities(doc, text)

def extract_entities(doc, text):
    entities = {"PRODUCT": [], "LOCATION": [], "ORDER_ID": [], "ORG": []}

    for ent in doc.ents:
        if ent.label_ == "LOC":
            entities["LOCATION"].append(ent.text)
        elif ent.label_ == "ORG":
            entities["ORG"].append(ent.text)
        elif ent.label_ == "MISC":
            entities["PRODUCT"].append(ent.text)

    # Order ID via regex
    order_ids = re.findall(r"\b\d{4,}\b", text)
    if order_ids:
        entities["ORDER_ID"].extend(order_ids)

    return entities

# --- Cerveau Nehanda ---
async def nehanda_brain_reply(user, message: str, token: Optional[str] = None) -> str:
    intent, source, entities = detect_intent_and_entities(message)

    if intent == "search_product":
        product = entities["PRODUCT"][0] if entities["PRODUCT"] else None
        if not product:
            return "Quel produit veux-tu que je cherche ?"
        results = await fetch_products(product)
        if results and len(results) > 0:
            names = [p["name"] for p in results[:3]]
            return f"({source}) J’ai trouvé {len(results)} résultats pour « {product} » : {', '.join(names)}."
        return f"Désolée, aucun produit trouvé pour « {product} »."

    elif intent == "track_order":
        order_id = entities["ORDER_ID"][0] if entities["ORDER_ID"] else None
        if not order_id:
            return "Peux-tu me donner ton numéro de commande ?"
        data = await fetch_order(order_id, token) if token else None
        if data:
            return f"Commande {order_id} : statut = {data.get('status')}."
        return f"Je n’ai pas trouvé la commande {order_id}."

    elif intent == "promo_info":
        promos = await fetch_promos()
        if promos and len(promos) > 0:
            names = [p["name"] for p in promos[:3]]
            return f"({source}) Actuellement en promo : {', '.join(names)}."
        return "Aucune promotion active pour l’instant."

    elif intent == "payment_info":
        return "Modes de paiement : Mobile Money et espèces à la livraison."

    elif intent == "support_request":
        return "Tu peux contacter le support via WhatsApp au +229..."

    else:
        return "Je suis spécialisée sur Tôswè (produits, commandes, paiements, promos). Ta question ne rentre pas dans ce cadre."


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


