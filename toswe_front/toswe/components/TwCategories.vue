<template>
  <section class=" py-16 text-black">
    <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-12">
      
      <!-- Texte -->
      <div class="flex-1">
        <h2 class="text-3xl md:text-5xl lg:text-6xl font-bold mb-6 font-[Kenia] text-[#7D260F] leading-tight">
          Des produits de toutes catégories de chez vous.
        </h2>
        <p class="font-[Kumbh_Sans] text-lg leading-relaxed">
          De la collecte à la livraison, Tôswè assure un transport fluide, rapide et géolocalisé
          de vos produits jusqu’au client final. Vendeurs, concentrez-vous sur vos ventes.
          Nous, on s'occupe du reste.
        </p>
      </div>

      <!-- Catégories -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-8 place-items-center flex-1">
        <TwCategory
          :image-src="imageUrl"
          category-name="Agriculture & agroalimentaire"
        />
        <TwCategory
          :image-src="imageUrl"
          category-name="Cuisine traditionnelle"
        />
        <TwCategory
          :image-src="imageUrl"
          category-name="Artisanat culturel"
        />
        <TwCategory
          :image-src="imageUrl"
          category-name="Cosmétiques naturels"
        />
      </div>

    </div>
  </section>
</template>


<script setup>
const imageUrl = new URL('@/public/images/img1.png', import.meta.url).href
</script>
