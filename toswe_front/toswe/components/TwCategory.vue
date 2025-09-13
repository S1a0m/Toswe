<template>
  <div class="flex justify-center items-center">
    <div
      class="group relative w-64 h-64 [perspective:1200px] transition-transform duration-500 hover:scale-105"
    >
      <!-- Corps du carton -->
      <div
        class="relative w-full h-full rounded-2xl shadow-xl overflow-hidden border border-[#b68c5a] bg-gradient-to-br from-[#e5c7a0] to-[#c49a6c]"
      >
        <!-- Texture kraft -->
        <div
          class="absolute inset-0 opacity-20 mix-blend-overlay"
          style="background-image: url('https://www.transparenttextures.com/patterns/cartographer.png');
                 background-size: 180px;"
        ></div>

        <!-- Couvercle -->
        <div
          class="absolute top-0 left-0 w-full h-1/2 bg-gradient-to-b from-[#d4af78] to-[#b68c5a] border-b border-[#8b5e3c] origin-top transition-transform duration-700 ease-out group-hover:-rotate-x-60 group-hover:scale-105 shadow-md"
          style="transform-style: preserve-3d;"
        >
          <!-- Texture -->
          <div
            class="absolute inset-0 opacity-25"
            style="background-image: url('https://www.transparenttextures.com/patterns/cartographer.png');
                   background-size: 180px;"
          ></div>
        </div>

        <!-- Face avant -->
        <div
          class="absolute bottom-0 left-0 w-full h-full flex flex-col items-center justify-center p-4 z-10"
        >
          <!-- Cercle pour l'image -->
          <div
            class="w-32 h-32 rounded-full overflow-hidden border-4 border-[#8b5e3c] shadow-lg bg-[#fff9f2]"
          >
            <img
              :src="imageSrc"
              alt="Catégorie"
              class="w-full h-full object-cover"
            />
          </div>
          <!-- Texte -->
          <p
            class="mt-4 font-extrabold text-xl text-center bg-gradient-to-r from-[#4b3621] to-[#a9744f] bg-clip-text text-transparent drop-shadow-md"
          >
            {{ categoryName }}
          </p>
        </div>

        <!-- Effet brillance -->
        <div
          class="absolute inset-0 bg-gradient-to-tr from-transparent via-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        ></div>
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
.group-hover\:-rotate-x-60:hover {
  transform: rotateX(-60deg);
}
</style>
