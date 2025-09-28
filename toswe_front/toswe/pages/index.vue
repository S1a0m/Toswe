<template>
  <section class="overflow-hidden">
    <Transition name="fade-slide" appear>
      <TwSubHeader v-if="show[0]" />
    </Transition>

    <Transition name="fade-slide" appear>
      <TwCategories v-if="show[1]" />
    </Transition>

    <Transition name="fade-slide" appear>
      <TwFeatures v-if="show[2]" />
    </Transition>

    <Transition name="fade-slide" appear>
      <TwBrandsCarousel v-if="show[3]" />
    </Transition>

    <Transition name="fade-slide" appear>
      <TwCta v-if="show[4]" />
    </Transition>

    <Transition name="fade-slide" appear>
      <TwMap v-if="show[5]" />
    </Transition>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue"

const show = ref([false, false, false, false, false, false])

onMounted(() => {
  // Affichage en cascade avec délai
  show.value.forEach((_, i) => {
    setTimeout(() => {
      show.value[i] = true
    }, i * 400) // délai de 400ms entre chaque composant
  })
})
</script>

<style scoped>
/* Transition fade + slide */
.fade-slide-enter-active {
  transition: all 0.6s ease;
}
.fade-slide-leave-active {
  transition: all 0.4s ease;
  opacity: 0;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
</style>
