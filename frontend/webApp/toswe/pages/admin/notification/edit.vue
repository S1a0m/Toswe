<template>
  <br><br><br>
  <div class="add-notification">
    <h1>Ajouter une notification</h1>

    <div class="form-section">
      <label for="title">Titre</label>
      <input id="title" v-model="title" type="text" placeholder="Titre de la notification" />

      <label for="description">Description</label>
      <textarea id="description" v-model="description" rows="4" placeholder="Contenu de la notification" />

      <label for="audience">Destinataires</label>
      <select id="audience" v-model="audienceMode">
        <option value="all">Tous les utilisateurs</option>
        <option value="selected">Sélectionner des utilisateurs</option>
      </select>

      <div v-if="audienceMode === 'selected'" class="user-list">
        <label>Utilisateurs :</label>
        <div v-for="user in allUsers" :key="user.id" class="user-checkbox">
          <input
            type="checkbox"
            :id="'user-' + user.id"
            :value="user.id"
            v-model="selectedUsers"
          />
          <label :for="'user-' + user.id">{{ user.name }}</label>
        </div>
      </div>

      <label for="status">État</label>
      <select id="status" v-model="status">
        <option value="draft">Brouillon</option>
        <option value="published">Publié</option>
        <option value="unpublished">Non publié</option>
      </select>

      <div class="form-actions">
        <button @click="submitNotification">Confirmer</button>
        <button class="cancel" @click="cancel">Annuler</button>
      </div>
    </div>
  </div><br><br><br><br><br><br><br><br><br>
</template>

<script setup>
import { ref } from 'vue'

// Champs de formulaire
const title = ref('')
const description = ref('')
const audienceMode = ref('all')
const status = ref('draft')
const selectedUsers = ref([])

// Simuler une liste d’utilisateurs pour l’exemple
const allUsers = ref([
  { id: 1, name: 'Alice Dupont' },
  { id: 2, name: 'Bruno Martin' },
  { id: 3, name: 'Chloé Bernard' },
  { id: 4, name: 'David Moreau' },
])

function submitNotification() {
  const payload = {
    title: title.value,
    description: description.value,
    status: status.value,
    recipients: audienceMode.value === 'all' ? 'all' : selectedUsers.value,
  }

  console.log('Notification à envoyer :', payload)
  // Tu peux envoyer `payload` à ton backend ici
}

function cancel() {
  title.value = ''
  description.value = ''
  audienceMode.value = 'all'
  selectedUsers.value = []
  status.value = 'draft'
}

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped lang="scss">
.add-notification {
  padding: 40px;
  max-width: 600px;
  margin: auto;
  background: rgba(245, 230, 218, 0.4);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);

  h1 {
    font-size: 24px;
    margin-bottom: 30px;
    color: #c0a080;
    text-align: center;
  }

  .form-section {
    display: flex;
    flex-direction: column;
    gap: 15px;

    label {
      font-weight: 600;
    }

    input[type="text"],
    textarea,
    select {
      padding: 10px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 10px;
      transition: border-color 0.2s ease;
      background: rgba(245, 230, 218, 0.4);

      &:focus {
        outline: none;
        border-color: #c0a080;
      }
    }

    .user-list {
      margin-left: 15px;

      .user-checkbox {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 5px;
      }
    }

    .form-actions {
      display: flex;
      justify-content: space-between;
      margin-top: 25px;

      button {
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s ease;

        &:first-of-type {
          background-color: #c0a080;
          color: white;

          &:hover {
            background-color: #a0785f;
          }
        }

        &.cancel {
          background: rgba(245, 230, 218, 0.4);

          &:hover {
            background-color: #e0e0e0;
          }
        }
      }
    }
  }
}
</style>
