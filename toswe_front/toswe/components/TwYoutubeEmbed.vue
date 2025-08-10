<template>
  <div class="relative w-full pt-[56.25%]"> <!-- 16:9 ratio -->
    <iframe
      class="absolute top-0 left-0 w-full h-full rounded-lg shadow-lg"
      :src="embedUrl"
      title="YouTube video player"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
    ></iframe>
  </div>
</template>

<script setup>
defineProps({
  videoId: {
    type: String,
    required: true
  },
  noCookie: {
    type: Boolean,
    default: false
  }
})

// Génère l'URL d'intégration YouTube (avec ou sans cookies)
const embedUrl = computed(() =>
  `https://${noCookie ? 'www.youtube-nocookie.com' : 'www.youtube.com'}/embed/${videoId}`
)
</script>
