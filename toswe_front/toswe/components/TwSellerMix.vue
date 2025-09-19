<template>
  <div
    class="relative w-full max-w-sm rounded-3xl overflow-hidden shadow-lg 
           group cursor-pointer transition-all duration-500 hover:shadow-2xl"
  >
    <!-- Label marque -->
    <div
      v-if="isBrand"
      class="absolute top-3 left-3 bg-gradient-to-r from-[#7D260F] to-[#A13B20] 
             text-white text-xs font-semibold px-2 py-0.5 rounded-full shadow-md z-10"
    >
      Marque
    </div>

    <!-- Image en fond -->
    <div class="relative w-full h-56">
      <img
        :src="imageSrc"
        :alt="shopName"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/40 to-transparent"></div>
    </div>

    <!-- Contenu -->
    <div
      class="absolute bottom-0 left-0 right-0 p-5 text-white 
             transition-all duration-500 group-hover:translate-y-[-15%]"
    >
      <!-- Nom boutique -->
      <div class="flex items-center">
        <h3 class="font-semibold text-lg sm:text-xl truncate">
          {{ shopName }}
        </h3>
        <span v-if="isVerified">
          <Icon
            name="mdi:check-decagram"
            class="inline-block w-5 h-5 text-blue-400 ml-1"
            title="Vendeur vérifié"
          />
        </span>
      </div>

      <!-- Abonnés -->
      <p class="text-sm opacity-90 mt-1">
        <span class="font-semibold text-[#FFB347]">{{ totalSubscribers }}</span>
        abonnés
      </p>

      <!-- ✅ Actions -->
      <div
        class="flex gap-3 mt-4 
               opacity-100 translate-y-0
               lg:opacity-0 lg:translate-y-5 
               lg:group-hover:opacity-100 lg:group-hover:translate-y-0 
               transition-all duration-500"
      >
        <!-- Bouton favoris -->
        <button
          class="flex items-center justify-center w-11 h-11 rounded-full 
                 bg-white/20 backdrop-blur-md border border-white/30 
                 text-white hover:bg-white/30 transition active:scale-95"
          @click.stop="toggleSubscribe"
          aria-label="S'abonner"
        >
          <Icon
            :name="isSubscribed ? 'heroicons:bell-slash-20-solid' : 'heroicons:bell-20-solid'"
            class="text-lg"
          />
        </button>

        <!-- Bouton visiter -->
        <button
          class="flex-1 px-5 py-2.5 bg-[#7D260F] text-white text-sm sm:text-base 
                 font-medium rounded-full shadow-md 
                 hover:bg-[#661f0c] transition active:scale-95"
          @click.stop="goToShopDetails(id)"
        >
          Visiter
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth"
import { useNavigation } from "@/composables/useNavigation"
import { ref, onMounted } from "vue"

const props = defineProps({
  id: { type: Number, required: true },
  imageSrc: { type: String, default: "/images/pagne.jpg" },
  shopName: { type: String, default: "Nom de la boutique" },
  totalSubscribers: { type: Number, default: 128 },
  initialSubscribed: { type: Boolean, default: false },
  isVerified: { type: Boolean, default: false },
  isBrand: { type: Boolean, default: false }
})

const auth = useAuthStore()
const isSubscribed = ref(props.initialSubscribed)
const totalSubscribers = ref(props.totalSubscribers)

// 🔹 Initialisation abonnement via GET
onMounted(async () => {
  if (auth.isAuthenticated) {
    try {
      const res = await $fetch(
        `http://127.0.0.1:8000/api/user/${props.id}/is-subscribed/`,
        {
          method: "GET",
          headers: { Authorization: `Bearer ${auth.accessToken}` }
        }
      )
      isSubscribed.value = res.subscribed
    } catch (err) {
      console.warn("Impossible de récupérer le statut abonnement", err)
    }
  }
})

const toggleSubscribe = async () => {
  if (!auth.isAuthenticated) {
    return alert("Vous devez être connecté pour vous abonner.")
  }

  try {
    const res = await $fetch(
      `http://127.0.0.1:8000/api/user/${props.id}/subscribe/`,
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
