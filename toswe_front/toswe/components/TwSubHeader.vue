<template>
  <section
    class="flex flex-col justify-center items-center min-h-[60vh] bg-[#7D260F] text-white font-[Kumbh_Sans] px-6 py-20"
  >
    <!-- Titre -->
    <h1 class="text-3xl md:text-4xl font-bold mb-12 text-center font-[Kenia]">
      Nous vendons pour vous.
    </h1>

    <!-- Actions -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-6xl">
      
      <!-- Carte Nehanda -->
      <div
        class="bg-white/90 backdrop-blur-lg text-[#7D260F] rounded-2xl p-6 flex flex-col items-center text-center shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 border border-white/30"
      >
        <img src="/assets/images/Nehanda.png" alt="Nehanda" class="w-full h-36 object-cover rounded-lg mb-4" />
        <Icon name="uil:robot" size="52" class="text-[#7D260F]" />
        <b class="text-lg mt-3">Faites vos emplettes avec Nehanda</b>
      </div>

      <!-- Carte Scanner (mise en avant) -->
      <div
        class="bg-gradient-to-br from-[#fff8f5] to-white text-[#7D260F] rounded-2xl p-6 flex flex-col items-center text-center shadow-lg hover:shadow-2xl hover:scale-110 transition-all duration-300 border-2 border-[#ffddc8]"
      >
        <img src="/assets/images/insta.jpeg" alt="Scanner" class="w-full h-36 object-cover rounded-lg mb-4" />
        <Icon name="uil:qrcode-scan" size="56" class="text-[#7D260F]" />
        <b class="text-lg mt-3">Scannez ou recherchez un produit</b>
        <span class="text-sm mt-2 text-[#7D260F]/70">Rapide. Simple. Intelligent.</span>
      </div>
      
      <!-- Carte Acheter -->
      <div
        class="bg-white/90 backdrop-blur-lg text-[#7D260F] rounded-2xl p-6 flex flex-col items-center text-center shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 border border-white/30"
      >
        <img src="/assets/images/img2.jpg" alt="Acheter" class="w-full h-36 object-cover rounded-lg mb-4" />
        <Icon name="uil:shopping-cart" size="52" class="text-[#7D260F]" />
        <b class="text-lg mt-3">Commencez vos achats</b>
      </div>
    </div>

    <!-- Accroche -->
    <p class="text-lg md:text-xl mt-10 max-w-3xl text-center leading-relaxed">
      Achetez local et optimisez votre activité grâce à nos solutions adaptées.<!-- : <span class="font-semibold">IA Nehanda</span> pour vous guider et <span class="font-semibold">Scanner intelligent</span> pour trouver vos produits en un instant.-->
    </p>
  </section>
</template>
