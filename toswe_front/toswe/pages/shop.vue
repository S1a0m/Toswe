<template>
  <section class="max-w-7xl mx-auto px-4 md:px-8 py-8">
    <!-- Résumé vendeur -->
    <div class="mb-8">
      <TwSellerSummary
        sellerName="Akossi"
        :sellerRating="4.5"
        :loyalCustomers="125"
      />
    </div>
    <h2 class="text-3xl font-bold text-center text-[#7D260F] mb-10 font-[Kenia]">
      Mes publicités
    </h2>
    <TwPendingValidations />
    <!-- Produits en vente -->
    <div class="pt-8 mt-8"> <!--border-t border-gray-200-->
    <h2 class="text-3xl font-bold text-center text-[#7D260F] mb-10 font-[Kenia]">
      Mes produits
    </h2>
    <TwProductsSellerFilter />
      <TwProducts title="" />
    </div>
  </section>
    <TwMenuSide />
    <TwCart />
</template>

<script setup>
</script>