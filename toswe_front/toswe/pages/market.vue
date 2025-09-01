<template>
    <TwMenuCategories />
    <TwMenuSide />
    <TwCart />
    <TwProducts title="Choisis pour vous"/>
    <div class="max-w-6xl mx-auto my-10 px-4 md:px-8">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-10 font-[Kenia]">
      Visitez la boutique de nos vendeurs
    </h2>
        <TwSellersMix />
    </div>
    <TwProducts title="D'autres clients ont aussi acheté ça"/>
    <div class="max-w-6xl mx-auto my-10 px-4 md:px-8">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-10 font-[Kenia]">
      Les produits de ces marques pourraient vous intéresser
    </h2>
        <TwBrands />
    </div>
    <!-- imageSrc="https://via.placeholder.com/300x200" -->
    <TwPopupAd
      
      title="Publicité Exemple"
      description="Découvrez nos nouveaux produits en promotion !"
      ctaText="Voir les offres"
      ctaLink="#"
      :delay="60000" 
    /><!-- 1 minute -->
</template>

<script setup>
/*const config = useRuntimeConfig();
const { data } = await useFetch('/users', {
  baseURL: config.public.apiBase
});*/
</script>
