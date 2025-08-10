<template>
  <div id="app" class="bg-[#fdf8f5] h-screen w-screen">
  <NuxtLoadingIndicator />
    <NuxtLayout>
      <transition name="page">
        <NuxtPage />
      </transition>
    </NuxtLayout>
  </div>
</template>