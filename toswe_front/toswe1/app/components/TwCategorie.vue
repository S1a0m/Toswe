<template>
  <div 
    class="relative w-48 h-48 group cursor-pointer" 
    style="perspective: 1000px;"
  >
    <!-- Couvercle du carton -->
    <div 
      class="absolute top-0 left-0 w-full h-14 bg-[var(--toswe-2)] border-b-4 border-[var(--toswe-3)] shadow-md origin-bottom transition-transform duration-500"
      :class="{ 'group-hover:open-lid': true }"
    ></div>

    <!-- Corps du carton -->
    <div class="absolute top-14 left-0 w-full h-[calc(100%-3.5rem)] bg-[var(--toswe-1)] border-2 border-[var(--toswe-3)] shadow-lg flex flex-col items-center justify-center p-2">
      <img 
        :src="image" 
        alt="Category" 
        class="w-16 h-16 object-contain"
      />
      <span class="mt-2 text-[var(--toswe-4)] font-bold text-lg">{{ name }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: String,
  image: String
})
</script>

<style scoped>
/* Rotation de couvercle */
.group:hover .open-lid {
  transform: rotateX(-55deg);
  transform-style: preserve-3d;
}
</style>
