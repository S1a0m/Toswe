<!-- TwProduct.vue -->
<template>
  <div
    class="group relative bg-gradient-to-br from-white/90 to-white/80 backdrop-blur-lg rounded-xl shadow-md border border-white/30 overflow-hidden hover:shadow-lg hover:scale-[1.02] transition-all duration-300 w-full"
    :class="{ 'border-yellow-400 shadow-yellow-200/50': isSponsored }"
  >
    <!-- Ruban Sponsorisé -->
    <div
      v-if="isSponsored"
      class="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-yellow-500 text-white text-[10px] font-bold px-2 py-1 rounded-bl-lg shadow-md uppercase tracking-wide"
    >
      Sponsorisé
    </div>

    <!-- Image compacte -->
    <div class="aspect-square bg-gray-50 overflow-hidden group">
      <img
        :src="`http://127.0.0.1:8000${imageSrc}/`"
        :alt="productName"
        @click="goToProductDetails(id)"
        class="size-full object-cover transform group-hover:scale-110 transition-transform duration-500 hover:cursor-pointer"
      />
      <span
        v-if="badge"
        class="absolute top-3 left-3 bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white text-xs font-semibold px-2 py-0.5 rounded-full shadow-md"
      >
        {{ badge }}
      </span>
    </div>

    <!-- Contenu compact -->
    <div class="p-3 flex flex-col gap-2">
      <!-- Nom -->
      <h3
        class="font-medium text-sm text-gray-900 truncate hover:cursor-pointer"
        @click="goToProductDetails(id)"
      >
        {{ productName }}
      </h3>
      <!-- Description -->
      <p class="text-xs text-gray-600 line-clamp-2">{{ description }}</p>

      <!-- Étoiles -->
      <div class="flex items-center gap-1">
        <Icon
          v-for="n in 5"
          :key="n"
          name="uil:star"
          size="14"
          :class="
            n <= Math.floor(rating)
              ? 'text-yellow-500'
              : n - rating < 1
              ? 'text-yellow-400/60'
              : 'text-gray-300'
          "
        />
        <span class="text-xs text-gray-500">({{ rating.toFixed(1) }})</span>
      </div>

      <!-- Prix + bouton -->
      <div class="mt-2 flex items-center justify-between">
        <span class="text-sm font-semibold text-[#7D260F]">{{ price }} FCFA</span>
        <button
          class="px-3 py-1.5 bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white text-xs font-semibold rounded-lg shadow-md hover:shadow-lg hover:from-[#A13B20] hover:to-[#7D260F] transition-all duration-300"
          :class="{ animate: isAnimating }"
          @click="handleAddClick"
        >
          {{ isAdded ? "Panier" : "Ajouter" }}
        </button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useCartStore } from '@/stores/cart'
import { useNavigation } from '@/composables/useNavigation'
import { useInteractionsStore } from '@/stores/interactions'

const { goToProductDetails } = useNavigation()

const props = defineProps({
  id: { type: Number, required: true },
  imageSrc: { type: String, default: '/images/img2.jpg' },
  productName: { type: String, default: 'Nom du produit' },
  description: { type: String, default: 'Courte description du produit.' },
  price: { type: Number, default: 3000 },
  rating: { type: Number, default: 4.5 },
  badge: { type: String, default: 'Nouveau' },
  isSponsored: { type: Boolean, default: false } // 👈 ajouté
})

const isAdded = ref(false)
const isAnimating = ref(false)

const cart = useCartStore()
const interactions = useInteractionsStore()

const product = {
  product_id: props.id,
  main_image: props.imageSrc,
  name: props.productName,
  price: props.price
}

function handleAddClick() {
  if (isAdded.value) {
    goToCart()
    return
  }

  cart.addToCart(product)
  interactions.addInteraction('add', props.id, "product added to cart")
  isAdded.value = true
  isAnimating.value = true

  setTimeout(() => {
    isAnimating.value = false
  }, 300)
}
</script>

<style scoped>

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