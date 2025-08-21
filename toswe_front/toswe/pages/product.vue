<template>
    <TwProductDetails />
    <TwComments />
    <TwProducts title="D'autres produits du même vendeur" />
    <span 
      @click="goToShop" 
      class="block w-fit mx-auto mt-6 px-4 py-2 text-center text-[#7D260F] font-medium 
            border border-[#7D260F]/30 rounded-xl 
            hover:bg-[#7D260F]/10 hover:text-[#5b1c0b] 
            transition-all duration-300 cursor-pointer shadow-sm"
    >
      🛍️ Visiter la boutique du vendeur
    </span>

    <TwProducts title="Produits similaires" />
    <TwMenuSide />
    <TwCart />
</template>

<script setup>
import { goToShop } from '@/utils/navigations'
</script>