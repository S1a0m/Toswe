from torch.nn.functional import cosine_similarity

def find_similar_products(query_image: Image.Image, top_k=5):
    embedder = ProductImageEmbedder()
    query_embedding = embedder.extract_embedding(query_image)

    index = build_index()

    similarities = []
    for product_id, emb in index:
        sim = cosine_similarity(query_embedding.unsqueeze(0), emb.unsqueeze(0)).item()
        similarities.append((product_id, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    top_ids = [pid for pid, score in similarities[:top_k]]
    from .models import Product
    return Product.objects.filter(id__in=top_ids)

