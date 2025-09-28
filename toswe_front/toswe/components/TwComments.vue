<template>
  <section class="max-w-6xl mx-auto mt-10 px-4">
    <!-- Titre -->
    <div class="flex items-center gap-2 mb-6">
      <Icon name="mdi:comment-text-outline" class="w-6 h-6 text-[#7D260F]" />
      <h3 class="text-xl font-bold text-[#7D260F]">
        Commentaire(s) ({{ feedbacks.results.length }})
      </h3>
    </div>

    <!-- Liste -->
    <div
      class="relative transition-all duration-500 ease-in-out"
      :class="expanded ? 'max-h-full' : 'max-h-40 overflow-hidden'"
    >
      <div class="space-y-4 mb-6">
        <TwComment
          v-for="(feedback, index) in feedbacks.results"
          :key="index"
          :username="feedback.user_name"
          :avatar="feedback.avatar"
          :content="feedback.comment"
          :date="feedback.created_at"
          :rating="feedback.rating"
        />
      </div>

      <!-- Dégradé -->
      <div
        v-if="!expanded && feedbacks.results.length > 1"
        class="absolute bottom-0 left-0 w-full h-16 bg-gradient-to-t from-white to-transparent"
      ></div>
    </div>

    <!-- Toggle -->
    <button
      v-if="feedbacks.results.length > 1"
      @click="expanded = !expanded"
      class="text-[#7D260F] font-medium mt-2 hover:underline"
    >
      {{ expanded ? 'Réduire' : 'Afficher plus' }}
    </button>

    <!-- Message si vide -->
    <p v-if="feedbacks.results.length === 0 && auth.isAuthenticated" class="text-gray-500">
      Soyez le premier à laisser un commentaire !
    </p>

    <!-- Si non connecté -->
     <div
    v-if="!auth.isAuthenticated"
    class="bg-[#FFF5F2] border border-[#F3D0C3] rounded-xl p-5 mt-6 text-center shadow-sm"
    >
      <p class="text-gray-700 text-sm md:text-base mb-3 flex items-center justify-center gap-2">
        <Icon name="uil:comment-alt-message" class="w-5 h-5 text-[#7D260F]" />
        Vous avez quelque chose à dire ?  
        <span class="font-semibold text-[#7D260F] ml-1">Connectez-vous</span> pour rejoindre la discussion !
      </p>

      <button
        @click="goToAuth"
        class="flex items-center justify-center gap-2 bg-[#7D260F] text-white px-5 py-2 rounded-lg font-medium shadow-md hover:bg-[#5c1c07] transition-colors duration-300 mx-auto"
      >
        <Icon name="uil:key-skeleton" class="w-5 h-5" />
        Se connecter
      </button>
    </div>


    <!-- Formulaire -->
    <form
      v-if="auth.isAuthenticated"
      @submit.prevent="addComment"
      class="bg-white p-5 border border-gray-200 rounded-xl shadow-sm space-y-4 mt-6"
    >
      <!-- Note -->
      <div class="flex items-center space-x-2">
        <span class="font-medium text-sm">Votre note :</span>
        <Icon
          v-for="n in 5"
          :key="n"
          :name="n <= newRating ? 'mdi:star' : 'mdi:star-outline'"
          class="w-6 h-6 cursor-pointer transition-colors duration-200"
          :class="n <= newRating ? 'text-yellow-500' : 'text-gray-300 hover:text-yellow-400'"
          @click="newRating = n"
        />
      </div>

      <!-- Texte -->
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
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const auth = useAuthStore()

const expanded = ref(false)
const route = useRoute() 

// Chargement du produit
const { data: feedbacks, pending, error } = await useAsyncData('feedback', () =>
  $fetch(`http://127.0.0.1:8000/api/feedback/?product=${route.query.id}`)
)

const newComment = ref('')
const newRating = ref(0)

async function addComment() {
  if (!newComment.value.trim() || newRating.value === 0) return

  try {
    const response = await $fetch('http://127.0.0.1:8000/api/feedback/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${auth.accessToken}`
      },
      credentials: 'include',
      body: {
        product: route.query.id,
        comment: newComment.value,
        rating: newRating.value
      }
    })

    feedbacks.value.results.push({
      user_name: response.user_name || 'Utilisateur Anonyme',
      avatar: '/images/default-avatar.png',
      comment: response.comment,
      created_at: response.created_at,
      rating: response.rating
    })

  newComment.value = ''
  newRating.value = 0
  } catch (error) {
    console.error('Erreur lors de l\'ajout du commentaire :', error)
  }
}
</script>
