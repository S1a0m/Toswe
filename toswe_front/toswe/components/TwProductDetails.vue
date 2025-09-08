<template>
  <section class="pt-10 max-w-6xl mx-auto px-4">
    <!-- Nom du produit -->
    <div class="flex gap-2">
      <h2 class="text-3xl font-bold mb-2 font-[Kenia] text-[#7D260F]">{{ product.name }}</h2>
      <span v-if="product.is_sponsored" class="text-sm font-semibold text-yellow-500 flex items-center gap-1 border border-yellow-400 rounded-full px-2 py-1 h-6"><Icon name="uil:megaphone" class="w-5 h-5 flex-shrink-0 transition-transform duration-300 group-hover:scale-110"/>Sponsorisé</span>
    </div>

    <!-- Prix et Note -->
    <div class="flex items-center space-x-6 mb-4">
      <span class="text-xl font-semibold text-[#7D260F]">{{ product.price }} fcfa</span>
      <div class="flex items-center space-x-1 text-yellow-500">
        <span class="font-semibold">{{ product.total_rating.average }}</span>
        <Icon name="uil:star" size="20" />
      </div>
    </div>

    <!-- Carrousel horizontal sur mobile, grille sur desktop -->
    <div class="flex md:grid md:grid-cols-3 gap-4 mb-8 overflow-x-auto md:overflow-visible no-scrollbar">
      <!-- Image produit 1 -->
      <img
      v-for="(value, index) in product.images"
        :src="value.image"
        :alt="`Image produit ${index + 1}`"
        class="w-64 md:w-full rounded-lg object-cover flex-shrink-0 cursor-zoom-in hover:opacity-95 transition"
        @click="openLightbox(index)"
      />

      <!-- Vidéo produit -->
      <div class="w-80 md:w-full aspect-video rounded-lg overflow-hidden flex-shrink-0">
        <iframe
          class="w-full h-full"
          src=""
          title="Vidéo produit"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>

    <!-- Description -->
    <p class="text-gray-700 leading-relaxed text-base">
      {{ product.description }}
    </p>

    <!-- Bouton Ajouter au panier -->
    <button
      class="w-full md:w-auto bg-[#7D260F] text-white font-semibold py-3 px-6 rounded-lg my-4 hover:bg-[#5c1c07] transition-colors duration-300 mb-8"
      :class="{ animate: isAnimating }"
      @click="handleAddClick"
    >
      {{ isAdded ? "Consulter le panier" : "Ajouter au panier" }}
    </button>

    <!-- LIGHTBOX -->
    <Teleport to="body">
      <transition name="fade">
        <div
          v-if="lightboxOpen"
          class="fixed inset-0 z-[9999] bg-black/80 backdrop-blur-sm flex items-center justify-center"
          @click.self="closeLightbox"
        >
          <!-- Close -->
          <button
            class="absolute top-4 right-4 rounded-full bg-white/20 hover:bg-white/30 text-white p-2"
            aria-label="Fermer"
            @click="closeLightbox"
          >
            ✕
          </button>

          <!-- Prev -->
          <button
            v-if="images.length > 1"
            class="absolute left-3 md:left-6 rounded-full bg-white/20 hover:bg-white/30 text-white p-3"
            aria-label="Précédent"
            @click.stop="prev"
          >
            ‹
          </button>

          <!-- Image -->
          <img
            :src="images[current].src"
            :alt="images[current].alt"
            class="max-w-[92vw] max-h-[90vh] rounded-lg shadow-2xl select-none"
            @click.stop="next"
          />

          <!-- Next -->
          <button
            v-if="images.length > 1"
            class="absolute right-3 md:right-6 rounded-full bg-white/20 hover:bg-white/30 text-white p-3"
            aria-label="Suivant"
            @click.stop="next"
          >
            ›
          </button>

          <!-- Compteur -->
          <div class="absolute bottom-4 text-white/80 text-sm">
            {{ current + 1 }} / {{ images.length }}
          </div>
        </div>
      </transition>
    </Teleport>
  </section>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute } from 'vue-router'
// import { useNavigation } from '@/composables/useNavigation'

const route = useRoute()
const cart = useCartStore()

// Chargement du produit
const { data: product, pending, error } = await useAsyncData('product', () =>
  $fetch(`http://127.0.0.1:8000/api/product/${route.query.id}/`),
)

// Emission de l'id du vendeur
const emit = defineEmits(['seller'])

watch(
  () => product.value,
  (newProduct) => {
    if (newProduct?.seller) {
      emit('seller', newProduct.seller)
    }
  },
  { immediate: true } // si jamais product est déjà dispo
)

// === état panier ===
const isAdded = ref(false)
const isAnimating = ref(false)

// ⚡ image principale
const main_image = computed(() => {
  if (!product.value?.images) return ''
  const main = product.value.images.find(img => img.is_main_image)
  return main ? main.image : product.value.images[0]?.image || ''
})

// ⚡ bouton ajouter
function handleAddClick() {
  if (!product.value) return

  if (isAdded.value) {
    goToCart()
    return
  }

  const productcart = {
    id: product.value.id,
    img: main_image.value,
    name: product.value.name,
    price: product.value.price
  }

  cart.addToCart(productcart)
  isAdded.value = true
  isAnimating.value = true

  setTimeout(() => {
    isAnimating.value = false
  }, 300)
}

// === Lightbox ===
const lightboxOpen = ref(false)
const current = ref(0)

const images = computed(() =>
  product.value?.images?.map((img, index) => ({
    src: img.image,
    alt: `Image produit ${index + 1}`
  })) || []
)

function openLightbox(index) {
  current.value = index
  lightboxOpen.value = true
  document.body.style.overflow = 'hidden'
}
function closeLightbox() {
  lightboxOpen.value = false
  document.body.style.overflow = ''
}
function next() {
  if (!images.value.length) return
  current.value = (current.value + 1) % images.value.length
}
function prev() {
  if (!images.value.length) return
  current.value = (current.value + images.value.length - 1) % images.value.length
}

// Raccourcis clavier
function onKey(e) {
  if (!lightboxOpen.value) return
  if (e.key === 'Escape') return closeLightbox()
  if (e.key === 'ArrowRight') return next()
  if (e.key === 'ArrowLeft') return prev()
}

onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>


<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

.fade-enter-from, .fade-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity .18s ease; }

button.animate {
  animation: bounce 0.3s ease;
}

@keyframes bounce {
  0% { transform: scale(1); }
  30% { transform: scale(1.15); }
  60% { transform: scale(0.95); }
  100% { transform: scale(1); }
}

</style>

