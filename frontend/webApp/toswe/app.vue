<script setup lang="ts">
// You might choose this based on an API call or logged-in status
const layout = "admin";
</script>

<template>
  <div id="app">
    <NuxtLayout>
      <transition name="page">
        <NuxtPage />
      </transition>
    </NuxtLayout>
  </div>
</template>

<style lang="scss">
*, body {
  margin: 0;
  padding: 0;
}

#app {
  background-image: url("/public/images/toswe-africa-art.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  // height: 100vh;
}

/* Transition de base */
.page-enter-active, .page-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

/* Début de l'animation d'entrée */
.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

/* Début de l'animation de sortie */
.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>