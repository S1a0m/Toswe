<template>
  <header class="sticky top-13 z-40 bg-white/70 backdrop-blur-md border-b border-[#e6d9d3] shadow-sm">
    <div class="max-w-6xl mx-auto px-4 py-5 flex items-center gap-5">
      <!-- Logo -->
      <div class="relative shrink-0">
        <img
          src="/images/yonapp.png"
          alt="Logo boutique"
          class="size-16 rounded-2xl object-cover border border-[#e6d9d3] shadow-sm"
        />
        <span
          v-if="shop.is_verified"
          class="absolute -bottom-1 -right-1 inline-flex items-center gap-1 rounded-full bg-emerald-600 text-white px-2 py-0.5 text-2xs shadow"
          title="Boutique vérifiée"
        >
          <i class="i-lucide-badge-check w-3 h-3"></i> Vérifié
        </span>
      </div>

      <!-- Infos -->
      <div class="min-w-0 flex-1">
        <div class="flex items-center gap-2 flex-wrap">
          <h1 class="text-2xl font-semibold truncate text-[#7D260F] font-[Kenia] tracking-tight">
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
        <div class="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-gray-700">
          <div class="inline-flex items-center gap-1">
            <span class="font-medium">{{ shop.stars_avg?.toFixed?.(1) || '—' }}</span>
            <span>⭐</span>
            <span class="text-gray-500">({{ shop.stars_count || 0 }} avis)</span>
          </div>

          <div class="w-px h-4 bg-gray-300" />

          <div class="inline-flex items-center gap-1">
            <span class="font-medium">{{ shop.loyal_customers_count || 0 }}</span>
            <span>abonnés</span>
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
          @click="$emit('contact')"
        >
          Contacter
        </button>
        <button
          v-if="!isOwner"
          class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition"
          @click="$emit('follow')"
        >
          Suivre
        </button>
        <NuxtLink
          v-else
          to="/dashboard/shop"
          class="px-4 py-2 rounded-xl border border-[#e6d9d3] text-gray-700 hover:bg-[#fdf8f5] transition"
        >
          Gérer ma boutique
        </NuxtLink>
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  shop: { type: Object, required: true },
  isOwner: { type: Boolean, default: false }
})
defineEmits(['contact', 'follow'])
</script>
