<template>
  <section class="pt-10 max-w-6xl mx-auto px-4">
    <!-- Nom du produit + Actions -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-3">
        <h2 class="text-3xl font-bold font-[Kenia] text-[#7D260F]">
          {{ product.name }}
        </h2>
        <span
          v-if="product.is_sponsored"
          class="flex items-center gap-1 text-xs font-medium bg-gradient-to-r from-yellow-400 to-yellow-500 text-white px-3 py-1 rounded-full shadow-sm"
        >
          <Icon name="mdi:bullhorn-outline" class="w-4 h-4" /> Sponsorisé
        </span>
      </div>

      <!-- ✅ Actions CRUD si propriétaire -->
      <div v-if="isOwner" class="flex items-center gap-2">
        <button
          @click="editProduct"
          class="p-2 flex items-center justify-center bg-white border border-[#e6d9d3] rounded-full shadow hover:bg-yellow-100 transition"
          title="Modifier"
        >
          <Icon name="mdi:pencil" size="18" class="text-yellow-600" />
        </button>
        <button
          @click="deleteProduct"
          class="p-2 flex items-center justify-center bg-white border border-[#e6d9d3] rounded-full shadow hover:bg-red-100 transition"
          title="Supprimer"
        >
          <Icon name="mdi:trash-can" size="18" class="text-red-600" />
        </button>
        <button
        v-if="!product.is_sponsored"
          @click="toggleSponsor"
          class="p-2 flex items-center justify-center bg-white border border-[#e6d9d3] rounded-full shadow hover:bg-blue-100 transition"
          title="Sponsoriser"
        >
          <Icon name="mdi:bullhorn" size="18" class="text-blue-600" />
        </button>
      </div>
    </div>

    <!-- Prix + Note -->
    <div class="flex items-center space-x-6 mb-6" v-if="product.promotion === null">
      <span class="text-2xl font-semibold text-[#7D260F]">
        {{ product.price }} fcfa
      </span>
      <div class="flex items-center space-x-1 text-yellow-500">
        <span class="font-semibold">{{ product.total_rating.average }}</span>
        <Icon name="mdi:star" size="22" />
      </div>
    </div>

    <!-- Prix + Promo + Note -->
    <div class="flex flex-col gap-2 mb-6" v-else>
      <div class="flex items-center space-x-4">
        <!-- Prix promo -->
        <div class="flex items-center gap-2">
          <span class="text-3xl font-bold text-[#7D260F]">
            {{ product.promotion.discount_price }} fcfa
          </span>
          <span class="text-sm text-gray-500 line-through">
            {{ product.price }} fcfa
          </span>
          <span class="bg-green-100 text-green-700 text-xs font-semibold px-2 py-0.5 rounded-full">
            {{ product.promotion.discount_percent }} % off
          </span>
        </div>

        <!-- Note -->
        <div class="flex items-center space-x-1 text-yellow-500">
          <span class="font-semibold">{{ product.total_rating.average }}</span>
          <Icon name="mdi:star" size="20" />
        </div>
      </div>

      <!-- Fin promo -->
      <div class="flex items-center gap-2 text-sm text-red-600 font-medium">
        <Icon name="mdi:clock-outline" size="18" />
        <span>Promo valable jusqu’au <strong>{{ product.promotion.ended_at }}</strong></span>
      </div>
    </div>

    <!-- Galerie -->
    <div class="flex md:grid md:grid-cols-3 gap-4 mb-8 overflow-x-auto md:overflow-visible no-scrollbar">
      <img
        v-for="(value, index) in product.images"
        :key="index"
        :src="value.image"
        :alt="`Image produit ${index + 1}`"
        class="w-64 md:w-full rounded-lg object-cover flex-shrink-0 cursor-zoom-in transition-transform duration-300 hover:scale-105 hover:shadow-lg"
        @click="openLightbox(index)"
      />
    </div>

    <!-- Description -->
    <p class="text-gray-700 leading-relaxed text-base mb-6">
      {{ product.description }}
    </p>

    <!-- ✅ Bouton Ajouter uniquement si ce n'est PAS le propriétaire -->
    <button
      v-if="!isOwner"
      class="w-full md:w-auto flex items-center justify-center gap-2 bg-[#7D260F] text-white font-semibold py-3 px-6 rounded-xl shadow-md hover:bg-[#5c1c07] transition-all duration-300"
      :class="{ animate: isAnimating }"
      @click="handleAddClick"
    >
      <Icon :name="isAdded ? 'mdi:cart-check' : 'mdi:cart-plus'" size="20" />
      {{ isAdded ? "Consulter le panier" : "Ajouter au panier" }}
    </button>

    <!-- Lightbox (inchangée) -->
    <Teleport to="body">
      <transition name="fade">
        <div
          v-if="lightboxOpen"
          class="fixed inset-0 z-[9999] bg-black/80 backdrop-blur-sm flex items-center justify-center"
          @click.self="closeLightbox"
        >
          <button
            class="absolute top-4 right-4 rounded-full bg-white/20 hover:bg-white/30 text-white p-2"
            aria-label="Fermer"
            @click="closeLightbox"
          >
            ✕
          </button>

          <button
            v-if="images.length > 1"
            class="absolute left-3 md:left-6 rounded-full bg-white/20 hover:bg-white/30 text-white p-3"
            aria-label="Précédent"
            @click.stop="prev"
          >
            ‹
          </button>

          <img
            :src="images[current].src"
            :alt="images[current].alt"
            class="max-w-[92vw] max-h-[90vh] rounded-lg shadow-2xl select-none"
            @click.stop="next"
          />

          <button
            v-if="images.length > 1"
            class="absolute right-3 md:right-6 rounded-full bg-white/20 hover:bg-white/30 text-white p-3"
            aria-label="Suivant"
            @click.stop="next"
          >
            ›
          </button>

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
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const cart = useCartStore()
const auth = useAuthStore()

const { data: product, pending, error } = await useAsyncData('product', () =>
  $fetch(`http://127.0.0.1:8000/api/product/${route.query.id}/`),
)

const isOwner = computed(() => auth?.user?.id === product.value?.seller_id)

const emit = defineEmits(['seller'])
watch(
  () => product.value,
  (newProduct) => {
    if (newProduct?.seller) emit('seller', newProduct.seller)
  },
  { immediate: true }
)

const isAdded = ref(false)
const isAnimating = ref(false)

const main_image = computed(() => {
  if (!product.value?.images) return ''
  const main = product.value.images.find(img => img.is_main_image)
  return main ? main.image : product.value.images[0]?.image || ''
})

function handleAddClick() {
  if (!product.value) return
  if (isAdded.value) return goToCart()

  cart.addToCart({
    id: product.value.id,
    img: main_image.value,
    name: product.value.name,
    price: product.value.price
  })

  isAdded.value = true
  isAnimating.value = true
  setTimeout(() => { isAnimating.value = false }, 300)
}

// === CRUD ===
function editProduct() {
  console.log('✏️ Éditer produit', product.value.id)
}
function deleteProduct() {
  if (confirm('Supprimer ce produit ?')) {
    console.log('🗑️ Supprimer produit', product.value.id)
  }
}
function toggleSponsor() {
  console.log('📢 Changer sponsorisation', product.value.id)
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
  current.value = (current.value + 1) % images.value.length
}
function prev() {
  current.value = (current.value + images.value.length - 1) % images.value.length
}

function onKey(e) {
  if (!lightboxOpen.value) return
  if (e.key === 'Escape') return closeLightbox()
  if (e.key === 'ArrowRight') return next()
  if (e.key === 'ArrowLeft') return prev()
}
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>
