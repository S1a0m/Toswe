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
    <SwiperSlide
      v-for="(seller, index) in sellers"
      :key="index"
      class="flex justify-center"
    >
      <TwSellerMix
        :id="seller.id"
        :seller-id="seller.seller_user_id"
        :image-src="seller.logo"
        :shop-name="seller.shop_name"
        :total-subscribers="seller.total_subscribers"
      />
    </SwiperSlide>
    <NuxtLink
      to="/sellers"
      class="absolute top-1/2 right-4 -translate-y-1/2 bg-white bg-opacity-70 hover:bg-opacity-100 text-gray-800 font-semibold py-2 px-4 rounded-full shadow-lg transition duration-300"
    >
      Voir tous les vendeurs
    </NuxtLink>
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
  $fetch('http://127.0.0.1:8000/api/user/sellers/')
)
</script>