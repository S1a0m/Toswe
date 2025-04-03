<script setup>
import { ref, computed } from "vue";

const showPopup = ref(true);
const searchQuery = ref("");

const results = ref([
  "Téléphone Android",
  "iPhone 13",
  "Casque Bluetooth",
  "Montre connectée",
  "Ordinateur portable",
  "Clavier mécanique",
  "Souris gaming",
]);

const filteredResults = computed(() => {
  if (!searchQuery.value) return [];
  return results.value.filter(item => 
    item.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const emit = defineEmits(['close-searchpopup']);

const closeSearchPopup = () => {
  emit('close-searchpopup');
};
</script>

<template>
    <div v-if="showPopup" class="popup-container">
      <div class="popup">
        <h1>Rechercher</h1>
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
        </div>
  
        <button class="close-btn" @click="closeSearchPopup">Fermer</button>
      </div>
    </div>
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
  </style>
  