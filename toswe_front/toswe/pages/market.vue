<template>
    <div class="mt-18">
        <TwMenuCategories />
    </div>
    <TwMenuSide />
    <TwCart />
    <TwProducts title="Mes produits"/>
    <div class="max-w-6xl mx-auto my-20">
    <h2 class="text-3xl font-bold text-center text-[#7D260F] mb-10 font-[Kenia]">
      Visitez la boutique de nos vendeurs
    </h2>
        <TwBrands />
    </div>
    <TwProducts title="D'autres clients ont aussi acheté ça"/>
    <div class="max-w-6xl mx-auto my-20">
    <h2 class="text-3xl font-bold text-center text-[#7D260F] mb-10 font-[Kenia]">
      Visitez la boutique de nos vendeurs
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