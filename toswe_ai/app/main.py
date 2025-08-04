import os
import django
import openai
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialiser Django pour accéder aux modèles
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nehanda.settings")
django.setup()

from products.models import Product  # Exemple: ton modèle Product dans l'app Django

# Initialiser FastAPI
app = FastAPI(title="Nehanda - Assistant IA", description="Assistant pour achats intelligents")

# Configuration OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Classe de requête pour FastAPI
class ChatRequest(BaseModel):
    message: str
    user_id: int = None  # facultatif

# Mémoire courte : historique des messages
history = []

# Détection de commandes (mots-clés)
def detect_command(text: str) -> str | None:
    triggers = {
        "commande": "passer_commande",
        "produits": "lister_produits",
        "payer": "expliquer_paiement",
    }
    for mot, action in triggers.items():
        if mot in text.lower():
            return action
    return None

# Fonction : générer réponse IA
def ask_nehanda(message: str, memory: list) -> str:
    messages = [{"role": "system", "content": "Tu es Nehanda, une assistante IA pour aider les gens à faire des achats intelligents. Tu as été développée par Toswè."}]
    messages += memory[-5:]  # garder le contexte (facultatif)
    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Fonction: accéder aux produits (Django)
def get_top_products(limit=5):
    produits = Product.objects.all()[:limit]
    return [{"nom": p.nom, "prix": p.prix} for p in produits]

# Endpoint principal
@app.post("/nehanda/chat")
async def chat(req: ChatRequest):
    user_message = req.message
    memory_entry = {"role": "user", "content": user_message}
    history.append(memory_entry)

    action = detect_command(user_message)

    if action == "lister_produits":
        produits = get_top_products()
        response = f"Voici quelques produits que je recommande :\n" + "\n".join(
            [f"- {p['nom']} : {p['prix']} FCFA" for p in produits])
    elif action == "passer_commande":
        response = "Pour passer une commande, veuillez cliquer sur le bouton 'Commander' sur le produit que vous souhaitez acheter."
    elif action == "expliquer_paiement":
        response = "Vous pouvez payer via Mobile Money, carte bancaire ou à la livraison. Souhaitez-vous une aide spécifique ?"
    else:
        response = ask_nehanda(user_message, history)

    history.append({"role": "assistant", "content": response})
    return {"reply": response}

