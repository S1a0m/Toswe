<template>
  <!-- 
    navigation --> <!-- vitesse du défilement (plus = plus lent) -->
  <Swiper
    :modules="[Autoplay]"
    :loop="true"
    :autoplay="{
      delay: 0,        // pas de pause entre les slides
      disableOnInteraction: false
    }"
    :speed="4000"       
    :slides-per-view="3"
    :space-between="20"
    grabCursor
    
  >
    <SwiperSlide
      v-for="(brand, index) in brands"
      :key="index"
      class="flex justify-center"
    >
      <TwBrand
        :image-src="brand.image"
        :brand-name="brand.name"
        :slogan="brand.slogan"
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