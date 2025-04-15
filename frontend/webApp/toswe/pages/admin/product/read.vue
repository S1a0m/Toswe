<template>
  <br><br><br>
  <div class="product-details-container">
    <header>
      <h2>Détails du produit</h2>
    </header>

    <div class="product-content">
      <div class="product-images">
        <div
          v-for="(image, index) in product.images"
          :key="index"
          class="image-wrapper"
        >
          <img :src="image" alt="Image du produit" />
        </div>
      </div>

      <div class="info">
        <div class="info-group">
          <span class="label">Nom :</span>
          <span class="value">{{ product.name }}</span>
        </div>

        <div class="info-group">
          <span class="label">Catégorie :</span>
          <span class="value">{{ product.category }}</span>
        </div>

        <div class="info-group">
          <span class="label">Descriptions :</span>
          <ul class="description-list">
            <li v-for="(desc, i) in product.descriptions" :key="i">
              {{ desc }}
            </li>
          </ul>
        </div>

        <div class="info-group">
          <span class="label">État :</span>
          <span class="value status" :class="product.status">{{ statusLabel(product.status) }}</span>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <button class="edit" @click="onEdit">Modifier</button>
      <button class="delete" @click="onDelete">Supprimer</button>
    </div>
  </div>
</template>

<script setup>
const product = {
  name: "Montre connectée élégante",
  category: "Accessoires",
  descriptions: [
    "Écran AMOLED",
    "Autonomie 7 jours",
    "Étanche 5 ATM",
    "Bracelet en cuir véritable"
  ],
  images: [
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/150/eeeeee",
    "https://via.placeholder.com/150/cccccc"
  ],
  status: "published" // 'draft', 'published', 'unpublished'
}

const statusLabel = (status) => {
  switch (status) {
    case 'draft': return 'Brouillon'
    case 'published': return 'Publié'
    case 'unpublished': return 'Non publié'
    default: return 'Inconnu'
  }
}

const onEdit = () => {
  // à remplacer par de la logique réelle
  alert("Édition du produit")
}

const onDelete = () => {
  const confirmed = confirm("Voulez-vous vraiment supprimer ce produit ?")
  if (confirmed) {
    alert("Produit supprimé")
  }
}

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped lang="scss">
.product-details-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 40px;
  background: rgba(245, 230, 218, 0.4);
  border-radius: 20px;
  backdrop-filter: blur(6px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Inter', sans-serif;

  header {
    margin-bottom: 30px;
    h2 {
      font-size: 28px;
      color: #C0A080;
      text-align: center;
    }
  }

  .product-content {
    display: flex;
    flex-direction: column;
    gap: 30px;

    .product-images {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      .image-wrapper {
        width: 100px;
        height: 100px;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }
    }

    .info {
      display: flex;
      flex-direction: column;
      gap: 16px;

      .info-group {
        display: flex;
        flex-direction: column;

        .label {
          font-weight: bold;
          color: #333;
        }

        .value {
          margin-top: 4px;
          color: #555;
          &.status {
            padding: 4px 10px;
            border-radius: 10px;
            display: inline-block;
            font-size: 14px;
            font-weight: 500;
            &.draft {
              background-color: #f0ad4e33;
              color: #d68f23;
            }
            &.published {
              background-color: #5cb85c33;
              color: #3c883c;
            }
            &.unpublished {
              background-color: #d9534f33;
              color: #a92e2a;
            }
          }
        }

        .description-list {
          margin-top: 4px;
          padding-left: 20px;
          li {
            color: #555;
            margin-bottom: 4px;
          }
        }
      }
    }
  }

  .action-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 40px;

    button {
      padding: 12px 24px;
      border-radius: 12px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s ease;

      &.edit {
        background-color: #C0A080;
        color: white;
        border: none;

        &:hover {
          background-color: #a88764;
        }
      }

      &.delete {
        background: transparent;
        color: #C0A080;
        border: 2px solid #C0A080;

        &:hover {
          background-color: rgba(192, 160, 128, 0.1);
        }
      }
    }
  }
}
</style>
