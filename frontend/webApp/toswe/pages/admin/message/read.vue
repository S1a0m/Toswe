<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Exemple de message récupéré (à remplacer par des données dynamiques)
const message = ref({})

const router = useRouter()
const route = useRoute()
const productId = route.query.id

async function fetchMessage() {
  const token = localStorage.getItem("access_token")

  try {
    const response = await fetch(`http://localhost:8000/admin/messages/${productId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (!response.ok) {
      throw new Error("Erreur lors de la réception.")
    }

    const data = await response.json()
    message.value = data


  } catch (error) {
    console.error(error)
    alert("Échec lors de la réception.")
  }
}

/*function formatDate(iso) {
  const date = new Date(iso)
  return date.toLocaleString('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}*/

async function deleteMessage() {
  const token = localStorage.getItem("access_token")

  try {
    const response = await fetch(`http://localhost:8000/admin/messages/${productId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    router.push('/admin/messages')

    if (!response.ok) {
      throw new Error("Erreur lors de la réception.")
    }

  } catch (error) {
    console.error(error)
    alert("Échec lors de la réception.")
  }
}

onMounted(() => {
  fetchMessage()
})

definePageMeta({
  layout: 'admin'
})
</script>

<template>
  <br><br><br>
  <br><br><br>
  <div class="message-read">
    <h1>Message reçu</h1>

    <div class="contact-info">
      <p><strong>Contact :</strong> {{ message.mail_or_number }}</p>
      <p><strong>Envoyé le :</strong> {{ message.time_sent }}</p>
    </div>

    <div class="content">
      <p><strong>Message :</strong></p>
      <p class="message-text">{{ message.content }}</p>
    </div>

    <div class="actions">
      <button @click="deleteMessage">Supprimer</button>
    </div>
  </div>
  <br><br><br>
  <br><br><br>
  <br><br><br>
  <br><br><br>
  <br><br><br>
</template>

<style scoped lang="scss">
.message-read {
  max-width: 700px;
  margin: 40px auto;
  padding: 30px;
  background: rgba(245, 230, 218, 0.4);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);

  h1 {
    text-align: center;
    color: #c0a080;
    margin-bottom: 25px;
  }

  .contact-info {
    margin-bottom: 25px;

    p {
      margin: 5px 0;
      font-size: 15px;
    }
  }

  .content {
    background: rgba(245, 230, 218, 0.4);
    padding: 20px;
    border-radius: 12px;

    .message-text {
      margin-top: 10px;
      white-space: pre-wrap;
    }
  }

  .actions {
    margin-top: 30px;
    text-align: right;

    button {
      background-color: #f44336;
      color: #fff;
      padding: 10px 25px;
      border: none;
      border-radius: 8px;
      cursor: pointer;

      &:hover {
        background-color: #d32f2f;
      }
    }
  }
}
</style>
