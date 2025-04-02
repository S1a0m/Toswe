<template>
    <div v-if="showPopup" class="popup-container">
      <div class="popup">
        <h1>Téléchargez notre application</h1>
        <p>Accédez à notre service en toute simplicité depuis votre mobile.</p>
        
        <div class="download-buttons">
          <div class="download-option">
            <a href="#" class="google-play">📲 Télécharger sur Google Play</a>
            <img src="/public/images/qr-code.png" alt="QR Code Android" class="qr-code" />
          </div>
          
          <div class="download-option">
            <a href="#" class="app-store">🍏 Télécharger sur l'App Store</a>
            <img src="/public/images/qr-code.png" alt="QR Code iOS" class="qr-code" />
          </div>
        </div>
  
        <button class="close-btn" @click="closePopup">Fermer</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const showPopup = ref(true);
  
  const closePopup = () => {
    showPopup.value = false;
  };
  </script>
  
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
  
  p {
    font-size: 18px;
    color: #F5E6DA;
  }
  
  .download-buttons {
    margin-top: 20px;
  }
  
  .download-option {
    margin-bottom: 15px;
  }
  
  .download-option a {
    display: block;
    padding: 12px;
    text-decoration: none;
    color: white;
    font-size: 16px;
    border-radius: 5px;
    text-align: center;
  }
  
  .google-play {
    background-color: #4285F4;
  }
  
  .app-store {
    background-color: #000;
  }
  
  .qr-code {
    margin-top: 10px;
    width: 100px;
    height: 100px;
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
  