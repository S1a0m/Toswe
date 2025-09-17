<!-- app.vue -->
<template>
  <div id="app" class="bg-[#fdf8f5] h-full w-full">
  <NuxtLoadingIndicator />
    <NuxtLayout>
      <transition name="page">
        <NuxtPage />
      </transition>
    </NuxtLayout>
  </div>
</template>