<template>
  <section class="mt-16 max-w-4xl mx-auto px-4">
    <!-- Nom du produit -->
    <h2 class="text-3xl font-bold mb-2 font-[Kenia] text-[#7D260F]">
      Manga
    </h2>

    <!-- Prix et Note -->
    <div class="flex items-center space-x-6 mb-4">
      <span class="text-xl font-semibold text-[#7D260F]">5000 fcfa</span>
      <div class="flex items-center space-x-1 text-yellow-500">
        <span class="font-semibold">4.5</span>
        <Icon name="uil:star" size="20" />
      </div>
    </div>

    <!-- Bouton Ajouter au panier -->
    <button
      class="w-full md:w-auto bg-[#7D260F] text-white font-semibold py-3 px-6 rounded-lg hover:bg-[#5c1c07] transition-colors duration-300 mb-8"
    >
      Ajouter au panier
    </button>

    <!-- Carrousel simple -->
    <div class="flex flex-col md:flex-row gap-4 mb-8">
      <img
        src="/assets/images/img2.jpg"
        alt="Image produit 1"
        class="w-full md:w-1/3 rounded-lg object-cover"
      />
      <img
        src="/assets/images/img1.png"
        alt="Image produit 2"
        class="w-full md:w-1/3 rounded-lg object-cover"
      />
      <div class="w-full md:w-1/3 aspect-video rounded-lg overflow-hidden">
        <iframe
          class="w-full h-full"
          src="https://www.youtube.com/embed/cduUZgrcOaU"
          title="Vidéo produit"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>

    <!-- Description -->
    <p class="text-gray-700 leading-relaxed text-base">
      Résistante à l’eau (IPX7) : Parfaite pour la plage, la piscine ou la douche.
          Mode Party Connect : Associez plusieurs enceintes pour une ambiance encore plus intense.
          Port USB & Micro SD : Lisez vos musiques directement sans Bluetooth.
          Bluetooth 5.0 : Connexion ultra-stable jusqu’à 15 mètres de distance.
          Autonomie longue durée : Jusqu’à 12 heures de musique non-stop avec une seule charge.
    </p>
    <button
      class="w-full md:w-auto bg-[#7D260F] text-white font-semibold py-3 px-6 rounded-lg hover:bg-[#5c1c07] transition-colors duration-300 my-8"
    >
      Voir la publicité
    </button>
  </section>
</template>
