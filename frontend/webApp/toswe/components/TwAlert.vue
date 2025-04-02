<template>
    <transition name="slide-up">
      <div v-if="showPopup" class="alert-popup">
        <img src="/public/images/info.jpg" alt="Information" class="alert-image" />
        <div class="alert-content">
          <p>Nouveauté ! Découvrez notre dernière mise à jour.</p>
          <a href="#" class="alert-btn">En savoir plus</a>
        </div>
      </div>
    </transition>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  const showPopup = ref(false);
  
  const displayPopup = () => {
    showPopup.value = true;
    setTimeout(() => {
      showPopup.value = false;
    }, 60000); // Disparait après 1 minute
  };
  
  onMounted(() => {
    displayPopup(); // Première alerte immédiate
    setInterval(displayPopup, 60000); // Répète chaque minute
  });
  </script>
  
  <style scoped>
  /* Animation d'apparition et disparition */
  .slide-up-enter-active,
  .slide-up-leave-active {
    transition: transform 0.5s ease-out, opacity 0.5s ease-in;
  }
  
  .slide-up-enter-from,
  .slide-up-leave-to {
    transform: translateY(100%);
    opacity: 0;
  }
  
  .alert-popup {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: #2D1B14;
    color: #F5E6DA;
    padding: 15px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    max-width: 300px;
  }
  
  .alert-image {
    width: 50px;
    height: 50px;
    border-radius: 5px;
  }
  
  .alert-content {
    flex-grow: 1;
  }
  
  .alert-btn {
    display: block;
    margin-top: 10px;
    text-decoration: none;
    background: #7D260F;
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    text-align: center;
  }
  
  .alert-btn:hover {
    background: #C0A080;
  }
  </style>
  