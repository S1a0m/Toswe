<template>
  <Swiper
    :modules="[Autoplay]"
    :speed="4000"
    :space-between="20"
    grabCursor
    :breakpoints="{
      320: { slidesPerView: 1 },   // Mobile : 1 carte
      640: { slidesPerView: 2 },   // Tablette : 2 cartes
      1024: { slidesPerView: 3 },  // Desktop : 3 cartes
      1280: { slidesPerView: 4 }   // Très grands écrans : 4 cartes
    }"
  >
    <!-- Slides vendeurs -->
    <SwiperSlide
      v-for="(seller, index) in sellers"
      :key="index"
      class="flex justify-center"
    >
      <TwSellerMix
        :id="seller.id"
        :image-src="seller.logo"
        :shop-name="seller.shop_name"
        :total-subscribers="seller.total_subscribers"
        :is-verified="seller.is_verified"
        :is-brand="seller.is_brand"
      />
    </SwiperSlide>

    <!-- Slide spécial "Voir plus" -->
    <SwiperSlide class="flex justify-center">
      <NuxtLink
        to="/sellers"
        class="flex flex-col items-center justify-center h-56 border-2 border-dashed border-[#7D260F]/40 hover:border-[#7D260F]  group bg-white 
        relative w-full max-w-sm rounded-3xl overflow-hidden shadow-lg 
           group cursor-pointer transition-all duration-500 hover:shadow-2xl"
      >
        <div class="flex items-center justify-center w-16 h-16 rounded-full bg-[#7D260F]/10 group-hover:bg-[#7D260F]/20 transition">
          <Icon name="uil:arrow-right" class="w-20 h-20 text-[#7D260F]" />
        </div>
        <p class="mt-4 font-semibold text-[#7D260F] group-hover:underline">
          Voir tous les vendeurs
        </p>
      </NuxtLink>
    </SwiperSlide>
  </Swiper>
</template>



<script setup>
/**
    :autoplay="{
      delay: 0,
      disableOnInteraction: false
    }" */
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay } from 'swiper/modules'

// Styles Swiper
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'swiper/css/autoplay'

// const imageUrl = new URL('@/assets/images/img1.png', import.meta.url).href

const { data: sellers, pending, error } = await useAsyncData('sellers', () =>
  $fetch('http://127.0.0.1:8000/api/seller/top-sellers/')
)
</script>