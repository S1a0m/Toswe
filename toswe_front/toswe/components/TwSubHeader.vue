<template>
  <section
    class="flex flex-col justify-center items-center min-h-[60vh] bg-[#7D260F] text-white font-[Kumbh_Sans] px-6 py-20 relative overflow-hidden"
  >
    <!-- Effet flou décoratif en arrière-plan -->
    <div class="absolute inset-0 "></div> <!--bg-white/10 backdrop-blur-sm-->

    <!-- Contenu principal -->
    <div class="relative z-10 flex flex-col items-center">
      <!-- Titre -->
      <h1 class="text-3xl md:text-4xl font-bold mb-12 text-center font-[Kenia] drop-shadow-lg">
        Nous vendons pour vous.
      </h1>

      <!-- Cartes -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl">
        
        <!-- Carte Nehanda -->
        <div
          class="bg-white/10 backdrop-blur-lg text-white rounded-2xl p-6 flex flex-col items-center text-center shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300 border border-white/20"
        >
          <img src="/assets/images/Nehanda.png" alt="Nehanda" class="w-full h-36 object-cover rounded-lg mb-4" />
          <Icon name="uil:robot" size="52" class="text-white" />
          <b class="text-lg mt-3">Faites vos emplettes avec Nehanda</b>
        </div>

        <!-- Carte Scanner -->
        <div
          class="bg-white/20 backdrop-blur-lg text-white rounded-2xl p-6 flex flex-col items-center text-center shadow-xl hover:shadow-2xl hover:scale-110 transition-all duration-300 border border-white/30"
        >
          <img src="/assets/images/insta.jpeg" alt="Scanner" class="w-full h-36 object-cover rounded-lg mb-4" />
          <Icon name="uil:qrcode-scan" size="56" class="text-white" />
          <b class="text-lg mt-3">Scannez ou recherchez un produit</b>
          <span class="text-sm mt-2 text-white/80">Rapide. Simple. Intelligent.</span>
        </div>

        <!-- Carte Acheter -->
        <div
          class="bg-white/10 backdrop-blur-lg text-white rounded-2xl p-6 flex flex-col items-center text-center shadow-xl hover:shadow-2xl hover:scale-105 transition-all duration-300 border border-white/20"
        >
          <img src="/assets/images/img2.jpg" alt="Acheter" class="w-full h-36 object-cover rounded-lg mb-4" />
          <Icon name="uil:shopping-cart" size="52" class="text-white" />
          <b class="text-lg mt-3">Commencez vos achats</b>
        </div>
      </div>

      <!-- Accroche -->
      <p class="text-lg md:text-xl mt-10 max-w-3xl text-center leading-relaxed text-white/90">
        Achetez local et optimisez votre activité grâce à nos solutions adaptées.
      </p>
    </div>
  </section>
</template>
