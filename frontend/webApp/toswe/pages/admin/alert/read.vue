<template>
  <br><br><br>
  <br><br><br>
  <div class="alert-details">
    <h1>Détails de l'alerte</h1>

    <div class="banner" v-if="alert.bannerUrl">
      <img :src="alert.bannerUrl" alt="Bannière de l'alerte" />
    </div>

    <div class="info">
      <p><strong>Description :</strong></p>
      <p class="description">{{ alert.description }}</p>

      <p><strong>État :</strong> <span :class="statusClass">{{ getStatusLabel(alert.status) }}</span></p>
    </div>

    <div class="actions">
      <button class="edit" @click="editAlert">Modifier</button>
      <button class="delete" @click="deleteAlert">Supprimer</button>
    </div>
  </div>
  <br><br><br>
  <br><br><br>
  <br><br><br>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Simulation des données de l'alerte
const alert = ref({
  id: 1,
  bannerUrl: '/images/info.jpg', // à remplacer dynamiquement
  description: 'Intervention d’urgence sur le serveur à 14h00. Merci de votre patience.',
  status: 'published',
})

const statusClass = computed(() => {
  return {
    draft: 'status-draft',
    published: 'status-published',
    unpublished: 'status-unpublished',
  }[alert.value.status]
})

function getStatusLabel(status) {
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

function editAlert() {
  // Redirection vers la page de modification
  router.push(`/alerts/${alert.value.id}/edit`)
}

function deleteAlert() {
  if (confirm('Voulez-vous vraiment supprimer cette alerte ?')) {
    console.log('Alerte supprimée :', alert.value.id)
    // Ici, tu peux faire appel à ton API pour supprimer l'alerte
    router.push('/alerts')
  }
}

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped lang="scss">
.alert-details {
  max-width: 700px;
  margin: 40px auto;
  padding: 30px;
  background: rgba(245, 230, 218, 0.4);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);

  h1 {
    text-align: center;
    color: #c0a080;
    margin-bottom: 30px;
  }

  .banner img {
    width: 100%;
    border-radius: 10px;
    margin-bottom: 20px;
    max-height: 300px;
    object-fit: cover;
    border: 1px solid #ccc;
  }

  .info {
    .description {
      background: rgba(245, 230, 218, 0.4);
      padding: 15px;
      border-radius: 10px;
      margin-bottom: 20px;
      white-space: pre-wrap;
    }

    .status-published {
      color: green;
      font-weight: bold;
    }

    .status-draft {
      color: orange;
      font-weight: bold;
    }

    .status-unpublished {
      color: red;
      font-weight: bold;
    }
  }

  .actions {
    display: flex;
    justify-content: space-between;
    margin-top: 30px;

    button {
      padding: 12px 25px;
      font-weight: bold;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      font-size: 15px;
    }

    .edit {
      background-color: #c0a080;
      color: #fff;

      &:hover {
        background-color: #a0805f;
      }
    }

    .delete {
      background-color: #f44336;
      color: #fff;

      &:hover {
        background-color: #d32f2f;
      }
    }
  }
}
</style>
