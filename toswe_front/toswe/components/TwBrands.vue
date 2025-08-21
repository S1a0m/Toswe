<template>
  <Swiper
    :modules="[Autoplay]"
    :loop="true"
    :autoplay="{
      delay: 0,
      disableOnInteraction: false
    }"
    :speed="4000"
    :space-between="20"
    grab-cursor
    :breakpoints="{
      320: { slidesPerView: 1 },   // Mobile : 1 carte
      640: { slidesPerView: 2 },   // Tablette : 2 cartes
      1024: { slidesPerView: 3 },  // Desktop : 3 cartes
      1280: { slidesPerView: 4 }   // Très grands écrans : 4 cartes
    }"
  >
    <SwiperSlide
      v-for="brand in brands?.results"
      :key="brand.id"
      class="flex justify-center"
    >
      <TwBrand
        :image-src="imageUrl"
        :brand-name="brand.racine_id"
        :slogan="brand.slogan"
        :rating="brand.rating"
      />
    </SwiperSlide>
  </Swiper>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay } from 'swiper/modules'

// Styles Swiper
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import 'swiper/css/autoplay'

import TwBrand from '~/components/TwBrand.vue'

// Image temporaire
const imageUrl = new URL('@/assets/images/img1.png', import.meta.url).href

// Récupération des marques
const { data: brands, pending, error } = await useAsyncData('brands', () =>
  $fetch('http://127.0.0.1:8000/api/brands/')
)
</script>
