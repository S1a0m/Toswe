<template>
  <main class="max-w-6xl mx-auto px-4 py-8">
    <h2 class="text-xl font-bold text-[#7D260F] mb-2 font-[Kumbh_Sans]">
      Nos vendeurs
    </h2>

    <!-- Liste -->
    <div
      v-if="loading"
      class="flex justify-center items-center py-20 text-gray-500"
    >
      Chargement...
    </div>

    <div
      v-else-if="sellers.length"
      class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-6"
    >
      <TwSellerMix
        v-for="seller in sellers"
        :key="seller.id"
        :id="seller.id"
        :seller-id="seller.seller_user_id"
        :image-src="seller.logo"
        :shop-name="seller.shop_name"
        :total-subscribers="seller.total_subscribers"
        :is-verified="seller.is_verified"
        :is-brand="seller.is_brand"
      />
    </div>

    <p v-else class="text-center text-gray-500 py-20">
      Aucun vendeur trouvé.
    </p>

    <p class="mt-6 text-sm text-gray-70">
      Vous êtes un vendeur ? Allez dans les <span @click="goToSettings" class="cursor-pointer text-[#7D260F] hover:underline">paramètres</span> de votre compte pour lancer votre boutique !
    </p>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue"
import TwSellerMix from "@/components/TwSellerMix.vue"
import { useAuthStore } from "@/stores/auth"

const sellers = ref([])
const loading = ref(true)

const auth = useAuthStore()

const fetchSellers = async () => {
  try {
    const res = await $fetch("http://127.0.0.1:8000/api/user/sellers/", {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
    sellers.value = res
  } catch (err) {
    console.error("Erreur lors du chargement des vendeurs:", err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchSellers)
</script>
