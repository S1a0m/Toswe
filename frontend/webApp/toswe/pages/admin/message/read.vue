<template>
  <br><br><br>
  <br><br><br>
  <div class="message-read">
    <h1>Message reçu</h1>

    <div class="contact-info">
      <p><strong>Nom :</strong> {{ message.senderName }}</p>
      <p><strong>Email :</strong> {{ message.senderEmail }}</p>
      <p><strong>Téléphone :</strong> {{ message.senderPhone }}</p>
      <p><strong>Envoyé le :</strong> {{ formatDate(message.sentAt) }}</p>
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

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Exemple de message récupéré (à remplacer par des données dynamiques)
const message = ref({
  id: 1,
  senderName: 'Jean Dupont',
  senderEmail: 'jean.dupont@example.com',
  senderPhone: '+33 6 12 34 56 78',
  content: 'Bonjour, j’aimerais avoir plus d’informations sur votre service.',
  sentAt: '2025-04-13T14:30:00Z',
})

const router = useRouter()

function formatDate(iso) {
  const date = new Date(iso)
  return date.toLocaleString('fr-FR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function deleteMessage() {
  if (confirm('Voulez-vous vraiment supprimer ce message ?')) {
    console.log('Message supprimé :', message.value.id)
    // Appel à l’API ou mutation ici
    router.push('/messages')
  }
}

definePageMeta({
  layout: 'admin'
})
</script>

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
