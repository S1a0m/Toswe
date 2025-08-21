<template>
  <section
    class="flex flex-col gap-5 p-6 bg-gradient-to-br from-white to-gray-50 border border-gray-200 rounded-2xl shadow-md hover:shadow-lg transition max-w-3xl"
  >
    <!-- Haut : avatar + infos -->
    <div class="flex items-center gap-5">
      <!-- Logo / avatar -->
      <img
        src="/assets/images/yonapp.png"
        alt="Logo de la boutique"
        class="w-20 h-20 rounded-xl object-cover border border-gray-200 shadow-sm"
      />

      <!-- Nom + stats -->
      <div class="flex flex-col gap-1">
        <h2 class="text-2xl font-bold text-gray-900 tracking-tight">
          {{ sellerName }}
        </h2>

        <!-- Rating -->
        <div class="flex items-center gap-2">
          <div class="flex">
            <Icon
              v-for="n in 5"
              :key="n"
              name="uil:star"
              class="w-5 h-5"
              :class="n <= Math.round(sellerRating) ? 'text-yellow-400' : 'text-gray-300'"
            />
          </div>
          <span class="text-sm text-gray-700 font-semibold">
            {{ sellerRating.toFixed(1) }} / 5
          </span>
        </div>

        <!-- Stats -->
        <div class="flex items-center gap-4 mt-1 text-xs text-gray-600">
          <span class="flex items-center gap-1">
            <Icon name="uil:box" class="w-4 h-4 text-[#7D260F]" />
            <span>15 produits en vente</span>
          </span>
          <span class="flex items-center gap-1">
            <Icon name="uil:users-alt" class="w-4 h-4 text-green-600" />
            <span>{{ loyalCustomers }} clients fidèles</span>
          </span>
        </div>
      </div>
    </div>

    <!-- Description -->
    <p class="text-gray-700 leading-relaxed text-sm">
      Bienvenue dans la boutique de <strong>{{ sellerName }}</strong> !
      Découvrez une sélection de produits de qualité soigneusement choisis pour vous.
      Profitez d'une expérience d'achat unique avec des conseils personnalisés et un
      service client réactif.
    </p>
  </section>
</template>

<script setup>
const props = defineProps({
  sellerName: { type: String, required: true },
  sellerRating: { type: Number, required: true },
  loyalCustomers: { type: Number, required: true }
})
</script>
