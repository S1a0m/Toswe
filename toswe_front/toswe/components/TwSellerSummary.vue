<template>
  <section class="flex flex-col gap-4 p-6 bg-white border border-gray-200 rounded-lg shadow-sm max-w-3xl">
    <!-- Haut : logo + infos -->
    <div class="flex items-center gap-4">
      <!-- Logo / avatar -->
      <img
        src="/assets/images/yonapp.png"
        alt="Logo de la boutique"
        class="w-16 h-16 rounded-full object-cover border border-gray-300"
      />

      <!-- Nom + note -->
      <div class="flex flex-col">
        <h2 class="text-2xl font-bold text-gray-900">{{ sellerName }}</h2>

        <div class="flex items-center gap-2 mt-1">
          <!-- Étoiles -->
          <Icon
            v-for="n in 5"
            :key="n"
            name="uil:star"
            class="w-4 h-4"
            :class="n <= Math.round(sellerRating) ? 'text-yellow-500' : 'text-gray-300'"
          />
          <!-- Note -->
          <span class="text-sm text-gray-600 font-medium">
            {{ sellerRating.toFixed(1) }} / 5
          </span>
        </div>

        <span class="text-xs text-gray-500">15 produits en vente</span>
      </div>
    </div>

    <!-- Description -->
    <p class="text-gray-700 leading-relaxed text-sm">
      Bienvenue dans la boutique de <strong>{{ sellerName }}</strong> !
      Découvrez une sélection de produits de qualité, soigneusement choisis pour vous.
      Profitez d'une expérience d'achat unique avec des conseils personnalisés et un
      service client réactif.
    </p>
  </section>
</template>

<script setup>
const props = defineProps({
  sellerName: { type: String, required: true },
  sellerRating: { type: Number, required: true }
})
</script>
