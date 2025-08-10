<template>
  <div class="flex flex-col items-center text-center bg-white rounded-lg shadow-md p-4 w-48 hover:shadow-lg transition-shadow duration-300">
    <img
      :src="imageSrc"
      :alt="brandName"
      class="w-24 h-24 object-contain mb-3"
    />
    <h3 class="font-bold text-lg text-gray-800">{{ brandName }}</h3>
    <p class="text-sm text-gray-500 italic">{{ slogan }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  imageSrc: {
    type: String,
    default: '/assets/images/img1.png'
  },
  brandName: {
    type: String,
    default: 'Nom de la marque'
  },
  slogan: {
    type: String,
    default: 'Votre slogan ici'
  }
})
</script>