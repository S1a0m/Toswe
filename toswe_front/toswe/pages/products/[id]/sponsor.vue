<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-xl font-bold text-[#7D260F] mb-4">
      Sponsoriser le produit
    </h1>
    <form @submit.prevent="submitSponsor" class="space-y-4">
      <label class="block text-sm font-medium">Durée (jours)</label>
      <input v-model="days" type="number" min="1"
        class="w-full rounded-lg border-gray-300 focus:ring-[#7D260F]" />

      <button type="submit"
        class="w-full py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700">
        Valider le sponsoring
      </button>
    </form>
  </div>
</template>

<script setup>
const route = useRoute()
const days = ref(7)

async function submitSponsor() {
  // TODO: API sponsor
  alert(`Produit ${route.params.id} sponsorisé pour ${days.value} jours ✅`)
}
</script>
