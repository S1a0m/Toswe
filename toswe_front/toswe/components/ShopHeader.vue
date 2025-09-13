<template>
  <header
    class="sticky top-13 z-40 bg-white/70 backdrop-blur-md border-b border-[#e6d9d3] shadow-sm"
  >
    <div class="max-w-6xl mx-auto px-4 py-5 flex items-center gap-5">
      <!-- Logo -->
      <div class="relative shrink-0">
        <img
          :src="`http://127.0.0.1:8000/${shop.logo_url || 'placeholder-shop.png'}`"
          alt="Logo boutique"
          class="size-16 rounded-2xl object-cover border border-[#e6d9d3] shadow-sm"
        />
        <span
          v-if="shop.is_verified"
          class="absolute -bottom-1 -right-1 inline-flex items-center gap-1 rounded-full bg-emerald-600 text-white px-0.5 py-0.5 text-2xs shadow"
          title="Boutique vérifiée"
        >
          <Icon name="mdi:check-decagram" class="w-3 h-3" />
        </span>
      </div>

      <!-- Infos -->
      <div class="min-w-0 flex-1">
        <div class="flex items-center gap-2 flex-wrap">
          <h1
            class="text-2xl font-semibold truncate text-[#7D260F] font-[Kenia] tracking-tight"
          >
            {{ shop.name }}
          </h1>
          <span
            v-if="isOwner"
            class="text-xs px-2 py-0.5 rounded-full border bg-[#fdf8f5] text-gray-700"
          >
            Mon espace
          </span>
        </div>
        <p
          v-if="shop.slogan"
          class="text-sm text-gray-600 mt-0.5 line-clamp-2"
        >
          {{ shop.slogan }}
        </p>

        <!-- Stats -->
        <div
          class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-gray-700"
        >
          <div class="inline-flex items-center gap-1">
            <span class="font-medium">{{ shop.stars_avg?.toFixed?.(1) || '—' }}</span>
            <span>⭐</span>
            <span class="text-gray-500">({{ shop.stars_count || 0 }} avis)</span>
          </div>

          <div class="w-px h-4 bg-gray-300" />

          <div class="inline-flex items-center gap-1">
            <span class="font-medium">{{ totalSubscribers }}</span>
            <span>abonné(s)</span>
          </div>

          <div v-if="shop.products_count" class="w-px h-4 bg-gray-300" />

          <div
            v-if="shop.products_count"
            class="inline-flex items-center gap-1"
          >
            <span class="font-medium">{{ shop.products_count }}</span>
            <span>produits</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="ml-auto flex items-center gap-2">
        <button
          v-if="!isOwner"
          class="px-4 py-2 rounded-xl border border-[#e6d9d3] text-[#7D260F] hover:bg-[#fdf8f5] transition"
          @click="toggleSubscribe"
        >
          {{ isSubscribed ? "Se désabonner" : "S'abonner" }}
        </button>
        <span
          v-else
          class="px-4 py-2 rounded-xl border border-[#e6d9d3] text-gray-700 hover:bg-[#fdf8f5] transition"
        >
          <NuxtLink to="/stats" v-if="auth.user.is_premium">Voir mes statistiques</NuxtLink>
          <NuxtLink to="/premium" v-else>Devenir vendeur premium</NuxtLink>
        </span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  shop: { type: Object, required: true },
  isOwner: { type: Boolean, default: false }
})

const auth = useAuthStore()

// état abonnements
const totalSubscribers = ref(props.shop.loyal_customers_count || 0)
const isSubscribed = ref(false) // on peut l’initialiser via API si besoin

const toggleSubscribe = async () => {
  if (!auth.isAuthenticated) {
    return alert('Vous devez être connecté pour vous abonner.')
  }

  try {
    const res = await $fetch(
      `http://127.0.0.1:8000/api/user/${props.shop.seller_user_id}/subscribe/`,
      {
        method: 'POST',
        headers: { Authorization: `Bearer ${auth.accessToken}` }
      }
    )

    isSubscribed.value = res.subscribed
    totalSubscribers.value += res.subscribed ? 1 : -1
  } catch (err) {
    alert('Erreur : ' + (err?.data?.detail || err.message))
  }
}
</script>
