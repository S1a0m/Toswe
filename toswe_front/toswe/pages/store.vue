<template>
  <section class="max-w-7xl mx-auto px-4 md:px-8 py-8 mt-18">
    <!-- Résumé vendeur -->
    <div class="mb-8">
      <TwSellerSummary
        sellerName="Akossi"
        :sellerRating="4.5"
      />
    </div>

    <!-- Produits du vendeur -->
    <div class="border-t border-gray-200 pt-8">
      <TwProducts title="Produits du vendeur" />
    </div>
  </section>
    <TwMenuSide />
    <TwCart />
</template>
