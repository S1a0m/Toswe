<template>
  <section class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6 text-gray-900">Votre commande</h2>

    <!-- Détails de la commande -->
    <div v-if="orderItems.length > 0">
      <TwCartItem
        v-for="(item, index) in orderItems"
        :key="index"
        :imageSrc="item.imageSrc"
        :productName="item.productName"
        :price="item.price"
        :quantity="item.quantity"
      />

      <!-- Total -->
      <div class="flex justify-between items-center mt-6 pt-4 border-t border-gray-200">
        <span class="text-lg font-semibold">Total :</span>
        <span class="text-xl font-bold text-[#7D260F]">
          {{ totalPrice.toLocaleString() }} FCFA
        </span>
      </div>

      <!-- Statut de la commande -->
      <div class="mt-6">
        <span class="text-sm text-gray-500">Statut de la commande :</span>
        <span class="font-semibold text-gray-900">En cours de traitement</span>
      </div>
    </div>

    <!-- Aucune commande -->
    <div v-else class="text-center text-gray-500 py-10">
      Aucune commande trouvée.
    </div>
  </section>
</template>

<script setup>
import TwCartItem from './TwCartItem.vue'

const orderItems = ref([
  { imageSrc: '/assets/images/img1.png', productName: 'Produit 1', price: 2500, quantity: 2 },
  { imageSrc: '/assets/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 }
])

const totalPrice = computed(() =>
  orderItems.value.reduce((total, item) => total + item.price * item.quantity, 0)
)
</script>
