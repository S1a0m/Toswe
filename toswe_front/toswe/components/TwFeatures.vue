<template>
  <section class="py-16 px-6 md:px-12 bg-white">
    <!-- Titre Section -->
    <h2
      class="text-3xl md:text-4xl font-bold mb-12 text-center text-[#7D260F] font-[Kenia] leading-tight"
    >
      Ce que vous propose Tôswè.
    </h2>

    <!-- Grid Features -->
    <div
      class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8"
    >
      <!-- Scanner -->
      <div
        class="group text-black border border-[#7D260F33] flex flex-col items-center text-center p-8 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 bg-white hover:bg-[#FFF8F6]"
      >
        <Icon name="uil:camera" size="56" class="mb-4 text-[#7D260F]" />
        <h3 class="text-lg font-semibold mb-3">Scanner intelligent</h3>
        <p class="text-gray-700 leading-relaxed">
          Scannez vos produits facilement avec notre technologie avancée pour
          des recherches ultra rapides et précises.
        </p>
      </div>

      <!-- IA -->
      <div
        class="group text-black border border-[#7D260F33] flex flex-col items-center text-center p-8 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 bg-white hover:bg-[#FFF8F6]"
      >
        <Icon name="uil:robot" size="56" class="mb-4 text-[#7D260F]" />
        <h3 class="text-lg font-semibold mb-3">Assistance IA (EIA)</h3>
        <p class="text-gray-700 leading-relaxed">
          Profitez d’une intelligence artificielle pour vous conseiller, trouver
          les meilleurs produits et optimiser vos emplettes.
        </p>
      </div>

      <!-- Livraison -->
      <div
        class="group text-black border border-[#7D260F33] flex flex-col items-center text-center p-8 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 bg-white hover:bg-[#FFF8F6]"
      >
        <Icon name="uil:truck" size="56" class="mb-4 text-[#7D260F]" />
        <h3 class="text-lg font-semibold mb-3">Livraison rapide</h3>
        <p class="text-gray-700 leading-relaxed">
          Faites livrer vos produits en un temps record avec suivi en temps réel
          pour une tranquillité d’esprit totale.
        </p>
      </div>

      <!-- Paiement sécurisé -->
      <div
        class="group text-black border border-[#7D260F33] flex flex-col items-center text-center p-8 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 bg-white hover:bg-[#FFF8F6]"
      >
        <Icon name="uil:shield-check" size="56" class="mb-4 text-[#7D260F]" />
        <h3 class="text-lg font-semibold mb-3">Paiement sécurisé</h3>
        <p class="text-gray-700 leading-relaxed">
          Réglez vos achats en toute sécurité grâce à nos solutions de paiement
          fiables et certifiées.
        </p>
      </div>
    </div>
  </section>
</template>
