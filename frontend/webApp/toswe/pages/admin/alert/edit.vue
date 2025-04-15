<template>
  <br><br><br>
  <br><br><br>
  <div class="add-alert">
    <h1>Créer une alerte</h1>

    <form @submit.prevent="submitAlert">
      <!-- Image bannière -->
      <div class="form-group">
        <label>Bannière de l'alerte</label>
        <input type="file" accept="image/*" @change="handleImageUpload" />
        <img v-if="bannerPreview" :src="bannerPreview" alt="Aperçu" class="preview" />
      </div>

      <!-- Description -->
      <div class="form-group">
        <label>Description de l'alerte</label>
        <textarea v-model="alert.description" rows="4" placeholder="Décrivez l'alerte ici..."></textarea>
      </div>

      <!-- État -->
      <div class="form-group">
        <label>État de l'alerte</label>
        <select v-model="alert.status">
          <option value="draft">Brouillon</option>
          <option value="published">Publié</option>
          <option value="unpublished">Non publié</option>
        </select>
      </div>

      <!-- Boutons -->
      <div class="form-actions">
        <button type="submit" class="confirm">Confirmer</button>
        <button type="button" class="cancel" @click="cancelAlert">Annuler</button>
      </div>
    </form>
  </div>
  <br><br><br>
  <br><br><br>
  <br><br><br>
</template>

<script setup>
import { ref } from 'vue'

const alert = ref({
  banner: null,
  description: '',
  status: 'draft',
})

const bannerPreview = ref(null)

function handleImageUpload(event) {
  const file = event.target.files[0]
  if (file) {
    alert.value.banner = file
    bannerPreview.value = URL.createObjectURL(file)
  }
}

function submitAlert() {
  console.log('Alerte soumise :', alert.value)
  // Tu peux envoyer les données via API ici
}

function cancelAlert() {
  alert.value = { banner: null, description: '', status: 'draft' }
  bannerPreview.value = null
}

definePageMeta({
  layout: 'admin'
})
</script>

<style scoped lang="scss">
.add-alert {
  max-width: 600px;
  margin: 40px auto;
  padding: 40px;
  background: rgba(245, 230, 218, 0.4);
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);

  h1 {
    text-align: center;
    color: #c0a080;
    margin-bottom: 30px;
  }

  .form-group {
    margin-bottom: 25px;

    label {
      display: block;
      margin-bottom: 8px;
      font-weight: bold;
    }

    input[type="file"] {
      display: block;
    }

    textarea,
    select {
      width: 100%;
      padding: 12px;
      border-radius: 8px;
      border: 1px solid #ccc;
      font-size: 14px;
      background: rgba(245, 230, 218, 0.4);
    }

    .preview {
      margin-top: 10px;
      max-width: 100%;
      max-height: 200px;
      border-radius: 10px;
      border: 1px solid #ccc;
    }
  }

  .form-actions {
    display: flex;
    justify-content: space-between;

    button {
      padding: 12px 25px;
      border: none;
      border-radius: 10px;
      font-weight: bold;
      font-size: 15px;
      cursor: pointer;

      &.confirm {
        background-color: #c0a080;
        color: #fff;

        &:hover {
          background-color: #a0805f;
        }
      }

      &.cancel {
        background: rgba(245, 230, 218, 0.4);
        color: #444;

        &:hover {
          background-color: #ddd;
        }
      }
    }
  }
}
</style>
