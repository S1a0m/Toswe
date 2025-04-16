<script setup>
import { ref } from "vue";
import { useCookie } from "#app";

const cookieConsent = useCookie("cookieConsent");
const anonUserId = useCookie("anonUserId"); // on utilisera ça pour stocker l'ID anonyme
const showPopup = ref(!cookieConsent.value);


const acceptCookies = async () => {
  try {
    const response = await $fetch("http://localhost:8000/api/anonyme-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({}), 
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la création de l'utilisateur anonyme.");
    }

    const data = await response.json();
    // console.log(data) -> { id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" }

    anonUserId.value = data.id;
    cookieConsent.value = "accepted";
    showPopup.value = false;
  } catch (err) {
    console.error(err);
  }
};

const declineCookies = () => {
  cookieConsent.value = "declined";
  showPopup.value = false;
};
</script>

<template>
  <div v-if="showPopup" class="cookie-container">
    <p>
      Ce site utilise des cookies pour améliorer votre expérience.
      <NuxtLink to="/rules">En savoir plus</NuxtLink>.
    </p>
    <button @click="acceptCookies">Accepter</button>
    <button @click="declineCookies">Refuser</button>
  </div>
</template>

  
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
    background: #C0A080;
  }
  </style>
  