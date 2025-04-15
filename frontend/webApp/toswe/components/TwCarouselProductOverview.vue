<template>
  <div class="carousel-container">
    <transition name="slide-horizontal" mode="out-in">
      <img
        :key="currentIndex"
        :src="props.slides[currentIndex].src"
        class="carousel-image"
      />
    </transition>
    <div class="carousel-indicators">
      <span
        v-for="(slide, i) in props.slides"
        :key="i"
        @click="currentIndex = i"
        class="indicator"
        :class="{ active: currentIndex === i }"
      ></span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Déclare la prop "slides"
const props = defineProps({
  slides: {
    type: Array,
    required: true
  }
})

const currentIndex = ref(0)
</script>

<style scoped>
.carousel-container {
  width: 400px;
  height: 400px;
  position: relative;
  overflow: hidden;
}

.carousel-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

/* Transition styles */
.slide-horizontal-enter-active,
.slide-horizontal-leave-active {
  transition: transform 0.5s ease;
  position: absolute;
}
.slide-horizontal-enter-from {
  transform: translateX(100%);
}
.slide-horizontal-leave-to {
  transform: translateX(-100%);
}

/* Indicators */
.carousel-indicators {
  position: absolute;
  bottom: 1rem;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.indicator {
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  background-color: white;
  opacity: 0.5;
  cursor: pointer;
}

.indicator.active {
  background-color: #2563eb;
  opacity: 1;
}
</style>
