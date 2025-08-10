# embeddings_indexer.py
import os
import torch
from .ml_model import ProductImageEmbedder
from .models import Product

def build_index():
    embedder = ProductImageEmbedder()
    index = []

    for product in Product.objects.exclude(image=None):
        image_path = product.image.path
        if os.path.exists(image_path):
            from PIL import Image
            img = Image.open(image_path).convert("RGB")
            emb = embedder.extract_embedding(img)
            index.append((product.id, emb))

    return index  # [(id, emb_tensor), ...]
