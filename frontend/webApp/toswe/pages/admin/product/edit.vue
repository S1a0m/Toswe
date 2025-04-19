<script setup>
definePageMeta({
  layout: 'admin'
})

import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const previews = ref([])
const productImg = ref([])
const productName = ref('')
const productPrice = ref('')
const productCategory = ref('')
const productDescription = ref('')
const productStatus = ref('')

const route = useRoute()
const productId = route.query.id
const isEditing = !!productId

// Liste des catégories et états
const categories = ref([
  { name: "Chez nous", value: "local" },
  { name: "Accessoires", value: "accessories" },
  { name: "Bureautique", value: "computer" },
  { name: "Mode", value: "fashion" },
  { name: "Sport", value: "sport" },
  { name: "Art", value: "art" },
])

const statuses = ref([
  { name: "Brouillon", value: "draft" },
  { name: "Publié", value: "published" },
  { name: "Non publié", value: "unpublished" },
])

// Fonction de prévisualisation des fichiers
function handleFiles(event) {
  previews.value = []
  productImg.value = []
  const files = event.target.files
  for (const file of files) {
    const url = URL.createObjectURL(file)
    previews.value.push(url)
    productImg.value.push(file)
  }
}

// Récupération des données si on édite un produit
async function fetchProductForEdit() {
  const token = localStorage.getItem("access_token")

  try {
    const response = await fetch(`http://localhost:8000/admin/products/${productId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) throw new Error("Erreur lors de la réception.")

    const data = await response.json()

    productName.value = data.name || ''
    productPrice.value = data.price || ''
    productCategory.value = data.category || ''
    productDescription.value = data.description || ''
    productStatus.value = data.status || ''
    previews.value = (data.images || []).map(img => `http://localhost:8000/${img}`)

  } catch (error) {
    console.error(error)
    alert("Échec lors de la réception.")
  }
}

// Appel automatique au montage
onMounted(() => {
  if (isEditing) {
    fetchProductForEdit()
  }
})

// Soumission du formulaire
async function submitForm(event) {
  event.preventDefault()
  const token = localStorage.getItem("access_token")

  const formData = new FormData()
  formData.append("name", productName.value)
  formData.append("price", productPrice.value)

  const selectedCategory = categories.value.find(c => c.value === productCategory.value)
  formData.append("category", selectedCategory ? selectedCategory.value : '')

  formData.append("description", productDescription.value)
  formData.append("status", productStatus.value)

  for (let i = 0; i < productImg.value.length; i++) {
    formData.append("images", productImg.value[i])
  }

  try {
    const response = await fetch(
      isEditing 
        ? `http://127.0.0.1:8000/admin/products/${productId}` 
        : "http://127.0.0.1:8000/admin/products",
      {
        method: isEditing ? "PUT" : "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      }
    )

    if (!response.ok) throw new Error("Erreur lors de l'envoi.")

    const result = await response.json()
    alert(`Produit ${isEditing ? "modifié" : "ajouté"} avec succès!`)
    
    // Reset si ajout
    if (!isEditing) {
      productName.value = ''
      productPrice.value = ''
      productCategory.value = ''
      productDescription.value = ''
      productStatus.value = ''
      productImg.value = []
      previews.value = []
    }

  } catch (error) {
    console.error(error)
    alert(`Échec de ${isEditing ? "la modification" : "l'ajout"} du produit.`)
  }
}
</script>


<template>
  <br><br><br>
  <div class="add-product-container">
    <header>
      <h2>{{ isEditing ? "Modifier le produit" : "Ajouter un produit" }}</h2>
    </header>

    <form class="product-form" @submit="submitForm">
      <div class="form-group">
        <label for="product-images">Images du produit</label>
        <input type="file" multiple accept="image/*" @change="handleFiles" />
        <div v-for="(image, index) in previews" :key="index" class="pre">
          <img :src="image" alt="preview" width="100" class="view" />
        </div>
      </div>

      <div class="form-group">
        <label for="product-name">Nom du produit</label>
        <input type="text" id="product-name" v-model="productName" placeholder="Nom..." />
      </div>

      <div class="form-group">
        <label for="product-price">Prix du produit</label>
        <input type="number" id="product-price" v-model="productPrice" placeholder="Prix..." />
      </div>

      <div class="form-group">
        <label for="product-category">Catégorie</label>
        <select id="product-category" v-model="productCategory">
          <option value="" disabled selected>Choisir une catégorie</option>
          <option v-for="category in categories" :key="category.value" :value="category.value">
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="product-description">Descriptions</label>
        <textarea id="product-description" v-model="productDescription" rows="4" placeholder="Décrivez le produit..."></textarea>
      </div>

      <div class="form-group">
        <label for="product-status">État du produit</label>
        <select id="product-status" v-model="productStatus">
          <option value="" disabled selected>Choisir un état</option>
          <option v-for="status in statuses" :key="status.value" :value="status.value">
            {{ status.name }}
          </option>
        </select>
      </div>

      <div class="form-buttons">
        <button type="submit" class="confirm">Confirmer</button>
        <button type="button" class="cancel">Annuler</button>
      </div>
    </form>
  </div>
  <br><br><br>
</template>



<style scoped lang="scss">
.add-product-container {
  max-width: 700px;
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

  .product-form {
    display: flex;
    flex-direction: column;
    gap: 25px;

    .form-group {
      display: flex;
      flex-direction: column;

      label {
        font-weight: 600;
        margin-bottom: 8px;
        color: #444;
      }

      input,
      select,
      textarea {
        padding: 12px 16px;
        border-radius: 12px;
        border: 1px solid #ccc;
        background: rgba(245, 230, 218, 0.4);
        font-size: 16px;
        transition: border-color 0.3s ease;

        &:focus {
          outline: none;
          border-color: #C0A080;
        }
      }

      textarea {
        resize: vertical;
      }

      .pre {
        display: flex;
        flex-direction: row;
        .view {
          margin-top: 10px;
          max-width: 100%;
          max-height: 200px;
          border-radius: 10px;
          border: 1px solid #ccc;
        }
      }
    }

    .form-buttons {
      display: flex;
      justify-content: space-between;
      gap: 20px;

      button {
        flex: 1;
        padding: 12px 16px;
        font-size: 16px;
        border-radius: 12px;
        cursor: pointer;
        transition: background 0.3s ease, color 0.3s ease;

        &.confirm {
          background-color: #C0A080;
          color: #fff;
          border: none;

          &:hover {
            background-color: #a88966;
          }
        }

        &.cancel {
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
}
</style>
