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
    grabCursor
    :breakpoints="{
      320: { slidesPerView: 1 },   // Mobile : 1 carte
      640: { slidesPerView: 2 },   // Tablette : 2 cartes
      1024: { slidesPerView: 3 },  // Desktop : 3 cartes
      1280: { slidesPerView: 4 }   // Très grands écrans : 4 cartes
    }"
  >
    <SwiperSlide
      v-for="(brand, index) in brands"
      :key="index"
      class="flex justify-center"
    >
      <TwSellerMix
        :image-src="brand.image"
        :brand-name="brand.name"
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

const imageUrl = new URL('@/assets/images/img1.png', import.meta.url).href

const brands = [
  { image: imageUrl, name: 'Marque 1', slogan: 'Toujours avec vous' },
  { image: imageUrl, name: 'Marque 2', slogan: 'L’excellence au quotidien' },
  { image: imageUrl, name: 'Marque 3', slogan: 'Votre confort, une priorité' },
  { image: imageUrl, name: 'Marque 4', slogan: 'Naturellement meilleur' },
  { image: imageUrl, name: 'Marque 5', slogan: 'Innovation et tradition' }
]
</script>