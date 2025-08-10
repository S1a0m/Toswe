<template>
  <section class="py-12">
    <div class="max-w-6xl mx-auto px-4 flex flex-col md:flex-row items-center gap-12">

<div class="flex-[1.2] max-w-xl">
  <h2 class="text-3xl md:text-5xl lg:text-6xl font-bold mb-6 font-[Kenia] text-[#7D260F] leading-tight">
    Vous êtes une marque ?
  </h2>
  <p class="font-[Kumbh_Sans] text-lg leading-relaxed">
    Ça tombe bien !
    <br />
    Tôswè met en avant les <i>marques locales</i> et leur donne les outils pour
    mieux vendre, mieux livrer, et mieux se connecter aux clients proches d’eux.
  </p>
</div>

<div class="flex-[0.8] max-w-2xl w-full">
  <Swiper
    :slides-per-view="1"
    :space-between="20"
    :autoplay="{ delay: 2000, disableOnInteraction: false }"
    :loop="true"
    :breakpoints="{
      640: { slidesPerView: 2 },
      1024: { slidesPerView: 3 }
    }"
    navigation
    pagination
    class="pb-8"
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
</div>


    </div>
  </section>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'

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
