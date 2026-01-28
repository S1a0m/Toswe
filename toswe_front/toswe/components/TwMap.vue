<template>
  <section class="py-12">
    <div class="max-w-6xl mx-auto px-4 flex flex-col lg:flex-row items-center gap-12">
      
      <!-- Texte -->
      <div class="flex-[1.2] w-full max-w-xl text-center lg:text-left">
        <h2 class="text-3xl md:text-5xl lg:text-6xl font-bold mb-6 font-[Kenia] text-[#7D260F] leading-tight">
          Où nous trouver ?
        </h2>
        <p class="font-[Kumbh_Sans] text-base sm:text-lg leading-relaxed">
          Tôswè connecte vendeurs et clients dans tout le Bénin.
          <br />
          Suivez notre présence sur la carte.
        </p>
      </div>

      <!-- Carte -->
      <div class="flex-[0.8] w-full max-w-2xl h-[400px] rounded-2xl overflow-hidden shadow-lg border border-gray-200">
        <!-- Exemple avec iframe Google Maps -->
        <iframe
          src="https://maps.google.com/maps?width=600&height=400&hl=en&q=Universite%20Abomey-Calavi&t=k&z=14&ie=UTF8&iwloc=B&output=embed"
          width="100%"
          height="100%"
          style="border:0;"
          allowfullscreen="true"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
        ></iframe>
      </div>

    </div>
  </section>
</template>
