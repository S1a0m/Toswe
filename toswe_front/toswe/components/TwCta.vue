<template>
  <section class="bg-[#7D260F] text-white py-16 px-6">
    <div class="max-w-4xl mx-auto text-center">
      <!-- Titre -->
      <h2 class="text-3xl md:text-4xl font-bold mb-4 font-[Kenia] leading-tight">
        Rejoignez la communauté Tôswè
      </h2>

      <!-- Sous-texte -->
      <p class="text-lg md:text-xl text-white/90 leading-relaxed mb-8 font-[Kumbh_Sans]">
        Inscrivez-vous dès aujourd’hui pour commencer vos achats, profitez des meilleures offres, et vendez vos produits en toute simplicité.
      </p>

      <!-- Boutons d'action -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <NuxtLink
          to="/inscription"
          class="bg-white text-[#7D260F] font-semibold py-3 px-8 rounded-lg shadow-md hover:shadow-xl transition-all duration-300"
        >
          S’inscrire
        </NuxtLink>
        <NuxtLink
          to="/boutique"
          class="bg-transparent border border-white font-semibold py-3 px-8 rounded-lg hover:bg-white hover:text-[#7D260F] transition-all duration-300"
        >
          Commencer mes achats
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
