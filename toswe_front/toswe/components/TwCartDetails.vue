<template>
  <section class="px-4 md:px-8 py-12 max-w-3xl mx-auto">
  <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">Votre panier</h2>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">

    <!-- Liste des articles -->
    <div v-if="cartItems.length > 0">
      <TwCartItem
        v-for="(item, index) in cartItems"
        :key="index"
        :imageSrc="item.imageSrc"
        :productName="item.productName"
        :price="item.price"
        :quantity="item.quantity"
        @increase="increaseQuantity(index)"
        @decrease="decreaseQuantity(index)"
        @remove="removeItem(index)"
      />

      <!-- Total -->
      <div class="flex justify-between items-center mt-6 pt-4 border-t border-gray-200">
        <span class="text-lg font-semibold">Total :</span>
        <span class="text-xl font-bold text-[#7D260F]">
          {{ totalPrice.toLocaleString() }} FCFA
        </span>
      </div>

      <!-- Bouton commander -->
      <div class="mt-6 text-right">
        <button
          class="bg-[#7D260F] text-white px-6 py-3 rounded-lg font-semibold hover:bg-[#5b1c0b] transition-colors"
        >
          Passer la commande
        </button>
      </div>
    </div>

    <!-- Panier vide -->
    <div v-else class="text-center text-gray-500 py-10">
      Votre panier est vide.
    </div>
  </div>
  </section>
</template>

<script setup>
import TwCartItem from './TwCartItem.vue'

const cartItems = ref([
  { imageSrc: '/assets/images/img1.png', productName: 'Produit 1', price: 2500, quantity: 2 },
  { imageSrc: '/assets/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { imageSrc: '/assets/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { imageSrc: '/assets/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { imageSrc: '/assets/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 },
  { imageSrc: '/assets/images/img2.jpg', productName: 'Produit 2', price: 5000, quantity: 1 }
])

const increaseQuantity = (index) => {
  cartItems.value[index].quantity++
}

const decreaseQuantity = (index) => {
  if (cartItems.value[index].quantity > 1) {
    cartItems.value[index].quantity--
  }
}

const removeItem = (index) => {
  cartItems.value.splice(index, 1)
}

const totalPrice = computed(() =>
  cartItems.value.reduce((total, item) => total + item.price * item.quantity, 0)
)
</script>
