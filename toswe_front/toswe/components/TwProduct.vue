<!--<TwProduct />-->
<template>
  <div
    class="relative group w-full max-w-xs rounded-2xl overflow-hidden shadow-md 
           bg-white/90 backdrop-blur-lg border border-white/20 
           hover:shadow-xl hover:-translate-y-1 transition-all duration-500"
    :class="{ 'border-yellow-400 shadow-yellow-200/40': isSponsored }"
  >
    <!-- Ruban Sponsorisé -->
    <div
      v-if="isSponsored"
      class="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-yellow-500 
             text-white text-[10px] font-bold px-2 py-1 rounded-bl-lg shadow-md uppercase tracking-wide z-10"
    >
      Sponsorisé
    </div>

    <!-- Image produit -->
    <div class="relative w-full h-48">
      <img
        :src="`http://127.0.0.1:8000${imageSrc}/`"
        :alt="productName"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110 cursor-pointer"
        @click="goToProductDetails(id)"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>

      <!-- Badge -->
      <span
        v-if="badge"
        class="absolute top-3 left-3 bg-gradient-to-r from-[#7D260F] to-[#A13B20] 
               text-white text-xs font-semibold px-2 py-0.5 rounded-full shadow-md"
      >
        {{ badge }}
      </span>

      <!-- ✅ Boutons CRUD (uniquement si propriétaire) -->
      <div
        v-if="isOwner"
        class="absolute top-3 right-3 flex flex-col gap-2 z-20"
      >
        <button
          @click.stop="editProduct"
          class="p-2 flex items-center justify-center bg-white/90 rounded-full shadow hover:bg-yellow-100 transition border border-[#e6d9d3]"
        >
          <Icon name="mdi:pencil" size="18" class="text-yellow-600" />
        </button>
        <button
          @click.stop="deleteProduct"
          class="p-2 flex items-center justify-center bg-white/90 rounded-full shadow hover:bg-red-100 transition border border-[#e6d9d3]"
        >
          <Icon name="mdi:trash-can" size="18" class="text-red-600" />
        </button>
      </div>
    </div>

    <!-- Contenu -->
    <div class="absolute bottom-0 left-0 right-0 p-4 text-white 
                transition-all duration-500 group-hover:translate-y-[-10%]">
      <h3
        class="font-semibold text-base truncate cursor-pointer"
        @click="goToProductDetails(id)"
      >
        {{ productName }}
      </h3>

      <p class="text-xs opacity-90 line-clamp-2">{{ description }}</p>

      <!-- Étoiles -->
      <div class="flex items-center gap-1 mt-1">
        <Icon
          v-for="n in 5"
          :key="n"
          name="uil:star"
          size="14"
          :class="
            n <= Math.floor(rating)
              ? 'text-yellow-400'
              : n - rating < 1
              ? 'text-yellow-300/60'
              : 'text-gray-400'
          "
        />
        <span class="text-xs opacity-80">({{ rating.toFixed(1) }})</span>
      </div>

      <!-- Prix + bouton Panier -->
      <div
        class="flex items-center justify-between mt-3 opacity-0 translate-y-5 
               group-hover:opacity-100 group-hover:translate-y-0 
               transition-all duration-500"
      >
        <span class="text-sm font-semibold text-yellow-300">{{ price }} FCFA</span>
        <button
          v-if="!isOwner"
          class="px-3 py-1.5 bg-gradient-to-r from-[#7D260F] to-[#A13B20] 
                 text-white text-xs font-semibold rounded-lg shadow-md 
                 hover:shadow-lg hover:from-[#A13B20] hover:to-[#7D260F] 
                 transition-all duration-300 active:scale-95"
          :class="{ animate: isAnimating }"
          @click.stop="handleAddClick"
        >
          {{ isAdded ? "Panier" : "Ajouter" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useInteractionsStore } from '@/stores/interactions'
import { useNavigation } from '@/composables/useNavigation'

const { goToProductDetails } = useNavigation()
const auth = useAuthStore()
const cart = useCartStore()
const interactions = useInteractionsStore()

const props = defineProps({
  id: { type: Number, required: true },
  sellerId: { type: Number, required: true },
  imageSrc: { type: String, default: '/images/img2.jpg' },
  productName: { type: String, default: 'Nom du produit' },
  description: { type: String, default: 'Courte description du produit.' },
  price: { type: Number, default: 3000 },
  rating: { type: Number, default: 4.5 },
  badge: { type: String, default: 'Nouveau' },
  isSponsored: { type: Boolean, default: false }
})

const isOwner = computed(() => auth?.user?.id === props.sellerId)

console.log('--- Debug Info ---')
console.log('isOwner:', isOwner.value, 'auth.user.id:', auth?.user?.id, 'props.sellerId:', props.sellerId)

const isAdded = ref(false)
const isAnimating = ref(false)

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
  interactions.addInteraction('add', props.id, 'product added to cart')
  isAdded.value = true
  isAnimating.value = true
  setTimeout(() => { isAnimating.value = false }, 300)
}

// ✅ Fonctions CRUD (placeholders)
function editProduct() {
  console.log('Éditer produit', props.id)
}
function deleteProduct() {
  if (confirm('Supprimer ce produit ?')) {
    console.log('Supprimer produit', props.id)
  }
}
</script>
