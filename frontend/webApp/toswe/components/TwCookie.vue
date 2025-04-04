<template>
    <div v-if="showPopup" class="cookie-container">
      <p>
        Ce site utilise des cookies pour améliorer votre expérience.
        <NuxtLink to="/politique-cookies">En savoir plus</NuxtLink>.
      </p>
      <button @click="acceptCookies">Accepter</button>
      <button @click="declineCookies">Refuser</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useCookie } from "#app";
  
  // Vérifie si un cookie de consentement existe déjà
  const cookieConsent = useCookie("cookieConsent");
  const showPopup = ref(!cookieConsent.value);
  
  // Fonction pour accepter les cookies
  const acceptCookies = () => {
    cookieConsent.value = "accepted";
    showPopup.value = false;
  };
  
  // Fonction pour refuser les cookies
  const declineCookies = () => {
    cookieConsent.value = "declined";
    showPopup.value = false;
  };
  </script>
  
  <style scoped>
  .cookie-container {
    position: fixed;
    bottom: 20px;
    left: 20px;
    right: 20px;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 5px;
    font-family: "Inter";
  }
  
  .cookie-container p {
    margin: 0;
  }
  
  .cookie-container a {
    color: #7D260F;
    text-decoration: underline;
  }
  
  .cookie-container button {
    margin-left: 10px;
    background: #7D260F;
    border: none;
    padding: 8px 15px;
    cursor: pointer;
    border-radius: 3px;
  }
  
  .cookie-container button:hover {
    background: #e6b800;
  }
  </style>
  