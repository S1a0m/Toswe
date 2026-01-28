<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto relative">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-8 font-[Kenia] tracking-tight">
      Votre panier
    </h2>

    <div class="bg-white shadow-2xl rounded-2xl p-6 md:p-8 space-y-6">
      <p class="text-gray-700 bg-gray-100 font-semibold p-1">Assurez-vous de bien choisir vos produits avant de passer commande. </p>
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
      <span class="font-semibold">01 54 14 12 87</span>.
    </p>

    <!-- 🔹 Overlay Spinner Global -->
    <div
      v-if="isLoading"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999]"
    >
      <div class="bg-white p-6 rounded-xl shadow-lg flex flex-col items-center gap-3">
        <svg class="w-10 h-10 text-[#7D260F] animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        <p class="text-gray-700 font-medium">Traitement de la commande...</p>
      </div>
    </div>

    <!-- Popup commande reçue  -->
<div
  v-if="showOrderOkPopup"
  class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
>
  <div class="bg-white rounded-2xl p-6 shadow-xl max-w-sm w-full relative">
    <button
      @click="showOrderOkPopup = false"
      class="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
    >
      ✕
    </button>
    <h2 class="text-lg font-semibold text-center mb-4">Félicitations !</h2>
    <div class="p-3 bg-green-100 rounded-lg text-center">
      <p class="">Nous avons bien reçu votre commande.</p>
      <p class="">Nous vous contacterons dans quelques instants pour finaliser la livraison.</p>
    </div>
    <div class="flex gap-2 mt-4">
      <!-- Télécharger -->
      <button 
        @click="showOrderOkPopup = false"
        class="flex-1 py-2 bg-[#7D260F] text-white rounded-lg flex items-center justify-center gap-1 hover:bg-[#A13B20] transition"
      >
        C'est compris
      </button>
    </div>

  </div>
</div>

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
const isLoading = ref(false) // 🔹 état loading global
const showOrderOkPopup = ref(false)

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

    //alert("Votre commande a bien été enregistrée ✅", response.message)

    showOrderOkPopup.value = true
    // cart.clearCart()

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
