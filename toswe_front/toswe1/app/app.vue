<template>
  <div id="app" class="bg-toswe-light">
  <NuxtLoadingIndicator />
    <NuxtLayout>
      <transition name="page">
        <NuxtPage />
      </transition>
    </NuxtLayout>
  </div>
</template>
