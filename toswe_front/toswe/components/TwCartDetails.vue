<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
  <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">Votre panier</h2>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">

    <!-- Liste des articles -->
    <div v-if="cart.items.length > 0">
      <TwCartItem
        v-for="(item, index) in cart.items"
        :key="index"
        :id="item.id"
        :imageSrc="item.img"
        :productName="item.name"
        :price="item.price"
        :quantity="item.quantity"
      />

      <!-- Total -->
      <div class="flex justify-between items-center mt-6 pt-4 border-t border-gray-200">
        <span class="text-lg font-semibold">Total :</span>
        <span class="text-xl font-bold text-[#7D260F]">
          {{ cart.totalAmount }} fcfa
        </span>
      </div>

      <!-- Bouton commander -->
      <div class="mt-6 text-right">
        <button
        @click="showPopup = true"
          class="bg-[#7D260F] text-white px-6 py-3 rounded-lg font-semibold hover:bg-[#5b1c0b] transition-colors"
        >
          Passer la commande
        </button>
      </div>
    </div>

    <!-- Panier vide -->
    <div v-else class="text-center text-gray-500 py-10">
      <Icon
        name="mdi:cart-outline"
        class="mx-auto mb-6 text-gray-400 animate-bounce-slow"
        style="font-size: 72px;"
      />
      <p class="text-lg font-medium text-gray-600">Votre panier est vide.</p>
    </div>

    <TwPopupPayment
      v-if="showPopup"
      :visible="showPopup"
      payment-type="premium"
      @close="showPopup = false"
      @pay="handlePayment"
    />

  </div>
  </section>
</template>

<script setup>
import TwCartItem from './TwCartItem.vue'

import { useCartStore } from "@/stores/cart"

definePageMeta({
  prerender: true
})

const cart = useCartStore()

const cartItems = ref([
  { id: 1, imageSrc: '/images/img1.png', productName: 'Produit 1', price: 2500, quantity: 2 },
  { id: 2, imageSrc: '/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { id: 3, imageSrc: '/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { id: 4, imageSrc: '/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { id: 5, imageSrc: '/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { id: 6, imageSrc: '/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 }
])

const showPopup = ref(false)
const isPremium = ref(false) // ou true si tu veux direct mode premium

function handlePayment(payload) {
  console.log("Paiement reçu :", payload)
  // payload = { method: "momo" | "cash", momoNumber: "229..." }
  // Ici tu envoies ça à ton API backend
  showPopup.value = false
}

</script>

<style scoped>
@keyframes bounceSlow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.animate-bounce-slow {
  animation: bounceSlow 2.5s infinite;
}
</style>
