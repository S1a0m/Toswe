<script setup>
import { ref, watch } from "vue"

const searchQuery = ref("")
const results = ref([])
const loading = ref(false)

const fetchProducts = async () => {
  if (searchQuery.value.trim() === "") {
    results.value = []
    return
  }

  loading.value = true

  const token = localStorage.getItem("access_token")

  try {
    const res = await fetch(`http://localhost:8000/admin/products/search?keyword=${encodeURIComponent(searchQuery.value)}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (!res.ok) throw new Error("Erreur lors de la recherche")

    const data = await res.json()
    results.value = data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

// Déclenche une requête dès que la recherche change (avec délai)
let debounceTimeout
watch(searchQuery, () => {
  clearTimeout(debounceTimeout)
  debounceTimeout = setTimeout(() => {
    fetchProducts()
  }, 300) // 300ms de délai
})

const showPopup = ref(true);

const emit = defineEmits(['close-searchpopup']);

const closeSearchPopup = () => {
  emit('close-searchpopup');
};
</script>

<template>
    <transition name="slide-up">
      <div v-if="showPopup" class="popup-container">
        <div class="popup">
          <!--<h1>Rechercher</h1>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Tapez votre recherche..." 
            class="search-input"
          />
          
          <div class="results">
            <p v-if="searchQuery && filteredResults.length === 0">Aucun résultat trouvé.</p>
            <ul v-else>
              <li v-for="(result, index) in filteredResults" :key="index">
                {{ result }}
              </li>
            </ul>
          </div>-->
            <h1>Rechercher</h1>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher un produit..."
              class="search-input"
            />
            <div v-if="loading">Chargement...</div>
            <ul v-else>
              <li v-for="product in results" :key="product.id">
                {{ product.name }}
              </li>
            </ul>
    
          <button class="close-btn" @click="closeSearchPopup">Fermer</button>
        </div>
      </div>
    </transition>
  </template>
  
  <style scoped>
  .popup-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 4;
    font-family: "Inter";
  }
  
  .popup {
    background: #2D1B14;
    color: #F5E6DA;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  h1 {
    color: #C0A080;
  }
  
  .search-input {
    width: 90%;
    padding: 10px;
    border-radius: 5px;
    border: none;
    margin-top: 10px;
    font-size: 16px;
  }
  
  .results {
    margin-top: 15px;
    text-align: left;
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    padding: 8px;
    background: #F5E6DA;
    color: #2D1B14;
    margin-top: 5px;
    border-radius: 5px;
  }
  
  .close-btn {
    margin-top: 20px;
    padding: 10px 15px;
    background: #7D260F;
    border: none;
    color: white;
    font-size: 16px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .close-btn:hover {
    background: #C0A080;
  }

  .slide-up-enter-active,
  .slide-up-leave-active {
    transition: transform 0.5s ease-out, opacity 0.5s ease-in;
  }
  
  .slide-up-enter-from,
  .slide-up-leave-to {
    transform: translateY(100%);
    opacity: 0;
  }
  </style>
  