from app.core.db import engine, Base
from app.models import user, product, order, order_item, notification, message, announcement

def init():
    print("🛠️  Création des tables dans la base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅  Création terminée.")

if __name__ == "__main__":
    init()
