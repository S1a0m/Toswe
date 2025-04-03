<template>
  <div v-if="showPopup" class="popup-container">
    <div class="popup">
      <h1>Téléchargez notre application</h1><br>
      <hr><br>
      <p>Accédez à notre service en toute simplicité depuis votre mobile.</p>
      
      <div class="download-buttons">
        <div class="download-option">
          <a href="#" class="google-play" @click="redirectToStore">📲 Télécharger sur Google Play</a>ou<br>
          <p>Scanner ce code QR si vous etes sur android</p>
          <img src="/images/qr-code.webp" alt="QR Code Android" class="qr-code" />
        </div>
        <br><br>
        <div class="download-option">
          <a href="#" class="app-store" @click="redirectToStore">🍏 Télécharger sur l'App Store</a>ou<br>
          <p>Scanner ce code QR si vous etes sur iphone</p>
          <img src="/images/qr-code.webp" alt="QR Code iOS" class="qr-code" />
        </div>
      </div>

      <button class="close-btn" @click="closePopup">Fermer</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const redirectToStore = () => {
  if (/Android/i.test(navigator.userAgent)) {
    window.open("https://play.google.com/store/apps/details?id=ton.app.id", "_blank");
  } else if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) {
    window.open("https://apps.apple.com/app/idtonappid", "_blank");
  } else {
    alert("Téléchargez notre application mobile depuis votre smartphone !\n\nL'experience est meilleure sur notre application.");
  }
};

const props = defineProps(["showPopup"]);  // Récupère la variable de app.vue
const emit = defineEmits(["close"]);       // Permet d'envoyer un événement à app.vue

const closePopup = () => {
  emit("close");
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
  z-index: 5;
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

h1, hr {
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
