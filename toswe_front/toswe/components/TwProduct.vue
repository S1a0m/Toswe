<template>
  <div
    class="bg-gradient-to-br from-white/90 to-white/80 backdrop-blur-lg rounded-2xl shadow-lg border border-white/30 overflow-hidden hover:shadow-2xl hover:scale-105 transition-all duration-300 w-full"
  >
    <!-- Image -->
    <div class="relative w-full h-48 overflow-hidden group">
      <img
        src="/assets/images/img2.jpg"
        :alt="productName"
        @click="goToProduct"
        class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500 hover:cursor-pointer"
      />
      <span
        v-if="badge"
        class="absolute top-3 left-3 bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white text-xs font-semibold px-3 py-1 rounded-full shadow-md"
      >
        {{ badge }}
      </span>
    </div>

    <!-- Contenu -->
    <div class="p-5 flex flex-col gap-3">
      <!-- Nom -->
      <h3 class="font-bold text-lg text-gray-900 line-clamp-1 hover:cursor-pointer"
      @click="goToProduct"
      >
        {{ productName }}
      </h3>
      <!-- Description -->
      <p class="text-sm text-gray-600 line-clamp-2">{{ description }}</p>

      <!-- Étoiles -->
      <div class="flex items-center gap-1">
        <Icon
          v-for="n in 5"
          :key="n"
          name="uil:star"
          size="18"
          :class="n <= Math.floor(rating) ? 'text-yellow-500' : (n - rating < 1 ? 'text-yellow-400/60' : 'text-gray-300')"
        />
        <span class="text-xs text-gray-500">({{ rating.toFixed(1) }})</span>
      </div>

      <!-- Prix -->
      <div class="flex items-center justify-between mt-2">
        <span class="text-xl font-bold text-[#7D260F]">{{ price }} fcfa</span>
        <button
          class="px-4 py-2 bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white text-sm font-semibold rounded-full shadow-md hover:shadow-lg hover:from-[#A13B20] hover:to-[#7D260F] transition-all duration-300"
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
import { goToProduct } from '@/utils/navigations';
import { useCartStore } from "@/stores/cart"


const props = defineProps({
  id: {
    type: Number,
    required: true
  },
  imageSrc: {
    type: String,
    default: '/images/img2.jpg'
  },
  productName: {
    type: String,
    default: 'Nom du produit'
  },
  description: {
    type: String,
    default: 'Courte description du produit.'
  },
  price: {
    type: Number,
    default: 3000
  },
  rating: {
    type: Number,
    default: 4.5
  },
  badge: {
    type: String,
    default: 'Nouveau'
  }
})

const isAdded = ref(false)
const isAnimating = ref(false)

const cart = useCartStore()

const product = {
    id: props.id,
    img: props.imageSrc,
    name: props.productName,
    price: props.price
}

function handleAddClick() {
  if (isAdded.value) {
    goToProduct()
    return
  }

  cart.addToCart(product)
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