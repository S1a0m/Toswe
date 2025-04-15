<template>
  <br><br><br><br><br><br>
  <div class="notification-details">
    <h1>Détails de la notification</h1>

    <div class="detail-box">
      <p><strong>Titre :</strong> {{ notification.title }}</p>
      <p><strong>Description :</strong> {{ notification.description }}</p>
      <p><strong>État :</strong> {{ formatStatus(notification.status) }}</p>
      <p><strong>Destinataires :</strong></p>
      <ul v-if="notification.recipients === 'all'">
        <li>Tous les utilisateurs</li>
      </ul>
      <ul v-else>
        <li v-for="id in notification.recipients" :key="id">
          {{ getUserName(id) }}
        </li>
      </ul>
    </div>

    <div class="actions">
      <button class="edit" @click="editNotification">Modifier</button>
      <button class="delete" @click="deleteNotification">Supprimer</button>
    </div>
  </div><br><br><br><br><br><br><br><br><br><br><br><br>
</template>

<script setup>
import { ref } from 'vue'

// Exemple de notification simulée (remplace ça avec une requête réelle)
const notification = ref({
  id: 1,
  title: 'Maintenance prévue',
  description: 'Une maintenance du système aura lieu samedi à 22h.',
  recipients: [1, 3],
  status: 'published', // draft | published | unpublished
})

// Liste simulée des utilisateurs
const allUsers = [
  { id: 1, name: 'Alice Dupont' },
  { id: 2, name: 'Bruno Martin' },
  { id: 3, name: 'Chloé Bernard' },
  { id: 4, name: 'David Moreau' },
]

function getUserName(id) {
  const user = allUsers.find(u => u.id === id)
  return user ? user.name : 'Inconnu'
}

function formatStatus(status) {
  switch (status) {
    case 'draft':
      return 'Brouillon'
    case 'published':
      return 'Publié'
    case 'unpublished':
      return 'Non publié'
    default:
      return status
  }
}

function editNotification() {
  console.log('→ Rediriger vers le formulaire de modification')
  // Exemple : router.push(`/notifications/edit/${notification.value.id}`)
}

function deleteNotification() {
  const confirmed = confirm('Êtes-vous sûr de vouloir supprimer cette notification ?')
  if (confirmed) {
    console.log(`→ Suppression de la notification ${notification.value.id}`)
    // Supprimer la notification depuis le backend ici
  }
}

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped lang="scss">
.notification-details {
  max-width: 600px;
  margin: 50px auto;
  background: rgba(245, 230, 218, 0.4);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);

  h1 {
    color: #c0a080;
    font-size: 24px;
    margin-bottom: 25px;
    text-align: center;
  }

  .detail-box {
    background: rgba(245, 230, 218, 0.4);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 30px;

    p {
      margin-bottom: 10px;
      font-size: 16px;
    }

    ul {
      list-style: disc;
      margin-left: 20px;
    }
  }

  .actions {
    display: flex;
    justify-content: space-between;

    button {
      padding: 10px 20px;
      font-weight: bold;
      font-size: 16px;
      border-radius: 10px;
      border: none;
      cursor: pointer;
      transition: background-color 0.2s;

      &.edit {
        background-color: #c0a080;
        color: white;

        &:hover {
          background-color: #a0785f;
        }
      }

      &.delete {
        background: rgba(245, 230, 218, 0.4);
        color: #b80000;

        &:hover {
          background-color: #ffcfcf;
        }
      }
    }
  }
}
</style>
