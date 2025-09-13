<template>
  <article
    class="group relative rounded-2xl border border-gray-200 bg-white shadow-md overflow-hidden hover:shadow-lg transition-all duration-300"
  >
    <!-- Bouton "..." menu -->
    <div class="absolute top-3 right-3 z-20">
      <button
        @click="toggleMenu"
        class="p-1.5 bg-white/80 backdrop-blur rounded-full shadow hover:bg-gray-100 transition flex items-center justify-center"
      >
        <Icon name="mdi:dots-vertical" class="w-5 h-5 text-gray-600" />
      </button>

      <!-- Menu flottant -->
      <div
        v-if="menuOpen"
        class="absolute right-0 mt-2 w-32 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-30"
      >
        <button
          @click="editAd"
          class="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 flex items-center gap-2"
        >
          <Icon name="mdi:pencil" class="w-4 h-4 text-blue-500" />
          Modifier
        </button>
        <button
          @click="deleteAd"
          class="w-full text-left px-3 py-2 text-sm hover:bg-gray-50 flex items-center gap-2"
        >
          <Icon name="mdi:trash-can" class="w-4 h-4 text-red-500" />
          Supprimer
        </button>
      </div>
    </div>

    <!-- Image -->
    <div class="relative aspect-[16/9] overflow-hidden">
      <img
        :src="ad.image || '/placeholder-banner.png'"
        alt="Publicité"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
      />

      <!-- Overlay gradient -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-black/10 to-transparent"></div>

      <!-- Badge sponsorisé -->
      <span
        v-if="ad.isSponsored"
        class="absolute top-3 left-3 bg-[#7D260F] text-white text-[10px] font-semibold px-2 py-0.5 rounded-full shadow-md uppercase tracking-wide"
      >
        Sponsorisé
      </span>
    </div>

    <!-- Contenu -->
    <div class="p-4">
      <h4
        class="text-base font-semibold text-gray-800 group-hover:text-[#7D260F] transition-colors truncate"
      >
        {{ ad.title || 'Publicité' }}
      </h4>
      <p class="text-sm text-gray-600 line-clamp-2 mt-1">
        {{ ad.description || 'Description de la publicité' }}
      </p>
    </div>
  </article>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  ad: {
    type: Object,
    required: true
  }
})

const menuOpen = ref(false)

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function editAd() {
  console.log('✏️ Modifier pub', props.ad.id)
  menuOpen.value = false
}

function deleteAd() {
  if (confirm('Supprimer cette publicité ?')) {
    console.log('🗑️ Supprimer pub', props.ad.id)
  }
  menuOpen.value = false
}
</script>
