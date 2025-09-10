<template>
  <div
    class="flex flex-col items-center text-center 
           bg-white/90 backdrop-blur-md
           rounded-3xl shadow-lg border border-gray-200 
           overflow-hidden w-full max-w-sm 
           hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
  >
    <!-- Image / Logo -->
    <div class="w-full h-44 flex items-center justify-center bg-gray-50">
      <img
        :src="imageSrc"
        :alt="shopName"
        class="w-full h-full object-contain p-4"
      />
    </div>

    <!-- Contenu -->
    <div class="p-6 w-full">
      <!-- Nom -->
      <h3 class="font-semibold text-lg sm:text-xl text-gray-900 truncate">
        {{ shopName }}
      </h3>

      <!-- Abonnés -->
      <p class="text-sm text-gray-600 mt-1">
        <span class="font-semibold text-[#7D260F]">{{ totalSubscribers }}</span> abonnés
      </p>

      <!-- Boutons -->
      <div class="flex gap-3 mt-5 justify-center">
        <!-- Bouton favoris -->
        <button
          class="flex items-center justify-center w-11 h-11 
                 rounded-full border border-[#7D260F] text-[#7D260F] bg-white
                 shadow-sm hover:bg-[#7D260F]/10 hover:shadow-md 
                 transition-all duration-300 active:scale-95 
                 focus:outline-none focus:ring-2 focus:ring-[#7D260F]/40"
          @click="toggleSubscribe"
          aria-label="S'abonner"
        >
          <Icon
            :name="isSubscribed ? 'uil:heart-alt' : 'uil:heart'"
            class="text-lg"
          />
        </button>

        <!-- Bouton visiter -->
        <button
          class="px-5 py-2.5 bg-[#7D260F] text-white text-sm sm:text-base font-medium 
                 rounded-full shadow-sm hover:shadow-md hover:bg-[#661f0c] 
                 transition-all duration-300 active:scale-95 
                 focus:outline-none focus:ring-2 focus:ring-[#7D260F]/40 flex items-center gap-1"
          @click="goToShopDetails(sellerId)"
        >
          Visiter
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth"
import { useNavigation } from '@/composables/useNavigation'
import { ref } from "vue"

const props = defineProps({
  id: { type: Number, required: true },
  sellerId: { type: Number, required: true },
  imageSrc: { type: String, default: "/images/pagne.jpg" },
  shopName: { type: String, default: "Nom de la boutique" },
  totalSubscribers: { type: Number, default: 128 },
  initialSubscribed: { type: Boolean, default: false }
})

const auth = useAuthStore()
const isSubscribed = ref(props.initialSubscribed)
const totalSubscribers = ref(props.totalSubscribers)

const toggleSubscribe = async () => {
  if (!auth.isAuthenticated) {
    return alert("Vous devez être connecté pour vous abonner.")
  }

  try {
    const res = await $fetch(
      `http://127.0.0.1:8000/api/user/${props.sellerId}/subscribe/`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${auth.accessToken}` }
      }
    )

    isSubscribed.value = res.subscribed
    totalSubscribers.value += res.subscribed ? 1 : -1
  } catch (err) {
    alert("Erreur : " + (err?.data?.detail || err.message))
  }
}

const { goToShopDetails } = useNavigation()
</script>
