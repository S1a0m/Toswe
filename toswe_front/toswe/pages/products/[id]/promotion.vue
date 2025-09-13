<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-xl font-bold text-[#7D260F] mb-4">
      Lancer une promotion
    </h1>
    <form @submit.prevent="submitPromotion" class="space-y-4">
      <label class="block text-sm font-medium">Réduction (%)</label>
      <input v-model="discount" type="number" min="1" max="90"
        class="w-full rounded-lg border-gray-300 focus:ring-[#7D260F]" />

      <button type="submit"
        class="w-full py-3 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700">
        Activer la promotion
      </button>
    </form>
  </div>
</template>

<script setup>
const route = useRoute()
const discount = ref(10)

async function submitPromotion() {
  // TODO: API promotion
  alert(`Produit ${route.params.id} en promo -${discount.value}% 💸`)
}
</script>
