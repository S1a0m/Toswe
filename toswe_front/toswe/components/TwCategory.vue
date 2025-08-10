<template>
  <div class="flex justify-center items-center">
    <div class="group relative w-64 h-64 [perspective:1000px]">
      <!-- Corps du carton -->
      <div class="relative w-full h-full bg-[#d2a679] rounded-sm shadow-lg overflow-hidden border border-[#a57c52]">
        <!-- Texture kraft -->
        <div
          class="absolute inset-0 opacity-30"
          style="background-image: url('https://www.transparenttextures.com/patterns/cartographer.png');
                 background-size: 200px;"
        ></div>

        <!-- Couvercle -->
        <div
          class="absolute top-0 left-0 w-full h-1/2 bg-[#c69c6d] border-b border-[#a57c52] origin-top transition-transform duration-500 ease-out shadow-md group-hover:-rotate-x-75"
          style="transform-style: preserve-3d;"
        >
          <div
            class="absolute inset-0 opacity-25"
            style="background-image: url('https://www.transparenttextures.com/patterns/cartographer.png');
                   background-size: 200px;"
          ></div>
        </div>

        <!-- Face avant -->
        <div class="absolute bottom-0 left-0 w-full h-full flex flex-col items-center justify-center p-3 z-10">
          <img :src="imageSrc" alt="Catégorie" class="w-32 h-32 object-cover rounded shadow-md border border-[#8b5e3c]" />
          <p class="mt-3 font-bold text-[#4b3621] text-lg text-center drop-shadow-md">{{ categoryName }}</p>
        </div>

        <!-- Arêtes -->
        <div class="absolute top-0 left-0 w-full h-full pointer-events-none">
          <div class="absolute top-0 left-0 w-full h-px bg-[#a57c52]"></div>
          <div class="absolute bottom-0 left-0 w-full h-px bg-[#a57c52]"></div>
          <div class="absolute top-0 left-0 h-full w-px bg-[#a57c52]"></div>
          <div class="absolute top-0 right-0 h-full w-px bg-[#a57c52]"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  imageSrc: {
    type: String,
    default: '/images/img2.jpg'
  },
  categoryName: {
    type: String,
    default: 'Catégorie'
  }
})
</script>

<style scoped>
.group-hover\:-rotate-x-75:hover {
  transform: rotateX(-75deg);
}
</style>
