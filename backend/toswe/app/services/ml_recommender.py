from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
from app.models.product import Product
from app.models.user import UserHistory

def recommend_products_for_user(db: Session, user_id: int, top_k: int = 5):
    history = db.query(UserHistory).filter(UserHistory.user_id == user_id).all()
    if not history:
        return db.query(Product).order_by(Product.created_at.desc()).limit(top_k).all()

    viewed_product_ids = [h.product_id for h in history]
    history_by_product_id = {h.product_id: h for h in history}
    all_products = db.query(Product).all()
    viewed_products = [p for p in all_products if p.id in viewed_product_ids]
    unviewed_products = [p for p in all_products if p.id not in viewed_product_ids]

    if not viewed_products or not unviewed_products:
        return db.query(Product).order_by(Product.created_at.desc()).limit(top_k).all()

    vectorizer = TfidfVectorizer(stop_words="english")
    corpus = [p.description or "" for p in viewed_products + unviewed_products]
    tfidf_matrix = vectorizer.fit_transform(corpus)
    viewed_vecs = tfidf_matrix[:len(viewed_products)]
    unviewed_vecs = tfidf_matrix[len(viewed_products):]
    similarity_matrix = cosine_similarity(unviewed_vecs, viewed_vecs)

    # Ajout: Comptage des catégories préférées
    category_counts = Counter([p.category for p in viewed_products if p.category])
    
    product_scores = []
    for i, unviewed in enumerate(unviewed_products):
        sim_scores = []
        for j, viewed in enumerate(viewed_products):
            h = history_by_product_id[viewed.id]
            time_score = min(h.time_spent / 60.0, 1.0)
            final_weight = 0.5 * h.interaction_score + 0.3 * time_score
            sim_scores.append(similarity_matrix[i, j] * final_weight)

        base_score = sum(sim_scores) / len(sim_scores)
        category_boost = category_counts.get(unviewed.category, 0) / max(category_counts.values() or [1])
        final_score = base_score + 0.2 * category_boost
        product_scores.append((unviewed, final_score))

    product_scores.sort(key=lambda x: x[1], reverse=True)
    return [p for p, _ in product_scores[:top_k]]
