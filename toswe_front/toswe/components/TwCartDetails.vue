<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-8 font-[Kenia] tracking-tight">
      Votre panier
    </h2>

    <div class="bg-white shadow-2xl rounded-2xl p-6 md:p-8 space-y-6">
      
      <!-- Liste des articles -->
      <div v-if="cart.items.length > 0" class="space-y-4">
        <TwCartItem
          v-for="(item, index) in cart.items"
          :key="index"
          :id="item.id"
          :product_id="item.product_id"
          :imageSrc="item.main_image"
          :productName="item.name"
          :price="item.price"
          :quantity="item.quantity"
        />

        <!-- Total -->
        <div class="flex justify-between items-center mt-6 pt-6 border-t border-gray-200">
          <span class="text-lg font-semibold text-gray-700">Total :</span>
          <span class="text-2xl font-extrabold text-[#7D260F]">
            {{ cart.totalAmount }} fcfa
          </span>
        </div>

        <!-- Bouton commander -->
        <div class="mt-6 text-right">
          <button
            @click="showPopup = true"
            :disabled="isLoading"
            class="bg-gradient-to-r from-[#7D260F] to-[#A13B20] text-white px-8 py-3 rounded-2xl font-semibold shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!isLoading">Passer la commande</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="w-5 h-5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
              </svg>
              Traitement...
            </span>
          </button>
        </div>
      </div>

      <!-- Panier vide -->
      <div v-else class="text-center py-16">
        <Icon
          name="mdi:cart-outline"
          class="mx-auto mb-6 text-gray-400 animate-bounce-slow"
          style="font-size: 80px;"
        />
        <p class="text-lg font-medium text-gray-600">
          Votre panier est vide.
        </p>
      </div>

      <!-- Popup paiement -->
      <TwPopupPayment
        v-if="showPopup"
        :visible="showPopup"
        payment-type="order"
        @close="showPopup = false"
        @pay="handlePayment"
      />

    </div>

    <!-- Texte d’aide -->
    <p class="mt-6 text-sm text-gray-700">
      Besoin d'aide ? Faites votre demande à 
      <strong @click="goToNehanda" class="cursor-pointer text-[#7D260F] hover:underline">
        Nehanda
      </strong> 
      ou contactez-nous via WhatsApp ou appel direct au : 
      <span class="font-semibold">01 90 00 00 00</span>.
    </p>
  </section>
</template>

<script setup>
import TwCartItem from './TwCartItem.vue'
import { useCartStore } from "@/stores/cart"
import { useAuthStore } from "@/stores/auth"

definePageMeta({
  prerender: true
})

const cart = useCartStore()
const auth = useAuthStore()
const showPopup = ref(false)
const isLoading = ref(false) // 🔹 état loading

async function handlePayment(payload) {
  isLoading.value = true
  try {
    const orderData = {
      phone_number: payload.phoneNumber,
      contact_method: payload.contactMethod,
      address: payload.address,
      items: cart.items.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity,
        price: item.price
      }))
    }

    const response = await $fetch("http://127.0.0.1:8000/api/order/", {
      method: "POST",
      body: orderData,
      headers: auth.isAuthenticated
        ? { Authorization: `Bearer ${auth.accessToken}` }
        : {},
    })

    alert("Votre commande a bien été enregistrée ✅", response.message)

  } catch (error) {
    console.error("Erreur lors de la commande :", error)
    alert("Une erreur est survenue. Veuillez réessayer.")
  } finally {
    showPopup.value = false
    isLoading.value = false
  }
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
