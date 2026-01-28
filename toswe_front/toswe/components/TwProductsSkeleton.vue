<template>
  <div class="max-w-6xl mx-auto px-4 md:px-8">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="i in 8"
        :key="i"
        class="h-48 rounded-xl bg-gray-200 animate-pulse"
      />
    </div>
  </div>
</template>
