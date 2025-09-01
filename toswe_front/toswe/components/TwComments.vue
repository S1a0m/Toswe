<template>
  <section class="max-w-6xl mx-auto mt-5 px-4">
    <!-- Titre -->
    <h3 class="text-xl font-bold text-[#7D260F] mb-6">Commentaires ({{ comments.length }})</h3>

    <!-- Liste des commentaires -->
    <div
      class="relative transition-all duration-500 ease-in-out"
      :class="expanded ? 'max-h-full' : 'max-h-40 overflow-hidden'"
    >
      <div class="space-y-4 mb-8">
        <TwComment
          v-for="(comment, index) in comments"
          :key="index"
          :username="comment.username"
          :avatar="comment.avatar"
          :content="comment.content"
          :date="comment.date"
          :rating="comment.rating"
        />
      </div>

      <!-- Gradient pour cacher le bas si pas expand -->
      <div
        v-if="!expanded"
        class="absolute bottom-0 left-0 w-full h-16 bg-gradient-to-t from-white to-transparent"
      ></div>
    </div>

    <!-- Bouton toggle -->
    <button
      v-if="comments.length > 1"
      @click="expanded = !expanded"
      class="text-[#7D260F] font-medium mt-2 hover:underline"
    >
      {{ expanded ? 'Réduire' : 'Afficher plus' }}
    </button>

    <!-- Formulaire -->
    <form
      @submit.prevent="addComment"
      class="bg-white p-4 border border-gray-200 rounded-lg shadow-sm space-y-4 mt-6"
    >
      <!-- Choix de la note -->
      <div class="flex items-center space-x-2">
        <span class="font-medium text-sm">Votre note :</span>
        <Icon
          v-for="n in 5"
          :key="n"
          name="uil:star"
          class="w-6 h-6 cursor-pointer transition-colors duration-200"
          :class="n <= newRating ? 'text-yellow-500' : 'text-gray-300 hover:text-yellow-400'"
          @click="newRating = n"
        />
      </div>

      <!-- Champ texte -->
      <textarea
        v-model="newComment"
        placeholder="Écrivez votre commentaire..."
        class="w-full border border-gray-300 rounded-lg p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-[#7D260F] focus:border-transparent"
        rows="3"
      ></textarea>

      <!-- Bouton -->
      <button
        type="submit"
        class="bg-[#7D260F] text-white font-semibold px-6 py-2 rounded-lg hover:bg-[#5c1c07] transition-colors duration-300"
      >
        Publier
      </button>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const expanded = ref(false)

const comments = ref([
  {
    username: 'Jean Dupont',
    avatar: '/images/img2.jpg',
    content: 'Super produit, la livraison était rapide et conforme à la description.',
    date: '08/08/2025',
    rating: 5
  },
  {
    username: 'Awa Koné',
    avatar: '/images/user2.jpg',
    content: 'Service client très réactif, je recommande vivement.',
    date: '09/08/2025',
    rating: 4
  },
  {
    username: 'Awa Koné',
    avatar: '/images/user2.jpg',
    content: 'Service client très réactif, je recommande vivement.',
    date: '09/08/2025',
    rating: 4
  }
])

const newComment = ref('')
const newRating = ref(0)

function addComment() {
  if (!newComment.value.trim() || newRating.value === 0) return

  comments.value.push({
    username: 'Utilisateur Anonyme',
    avatar: '/images/default-avatar.png',
    content: newComment.value,
    date: new Date().toLocaleDateString(),
    rating: newRating.value
  })

  newComment.value = ''
  newRating.value = 0
}
</script>
