<template>
  <header
    :class="[
      'fixed top-0 left-0 w-full z-[1000] text-white shadow-md backdrop-blur-md transition-all duration-300',
      isScrolled ? 'bg-[#6B1F0D]/80 py-2' : 'bg-[#7D260F]/60 py-4'
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center">
        
        <!-- Logo -->
        <div class="flex items-center space-x-3">
          <img src="/assets/images/logo.png" alt="Tôswè" class="h-8 w-auto" />
          <span class="font-bold text-xl font-[Kumbh_Sans] tracking-wide">Tôswè</span>
        </div>

        <!-- Menu desktop -->
        <nav class="hidden md:flex items-center space-x-6 text-base">
          <button
            class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-white/10 transition"
          >
            <span class="font-[Kumbh_Sans]">Connexion / Inscription</span>
            <Icon name="uil:user" size="20" />
          </button>
          <button
            class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition"
            aria-label="Basculer en mode sombre"
          >
            <Icon name="uil:moon" size="20" />
          </button>
        </nav>

        <!-- Burger mobile -->
        <button
          @click="isOpen = !isOpen"
          class="md:hidden p-2 rounded-md hover:bg-white/10 transition"
          aria-label="Menu mobile"
        >
          <Icon :name="isOpen ? 'uil:times' : 'uil:bars'" size="26" />
        </button>
      </div>
    </div>

    <!-- Menu mobile -->
    <transition name="slide">
      <div
        v-if="isOpen"
        class="md:hidden bg-[#7D260F]/90 backdrop-blur-lg shadow-md flex flex-col items-start p-4 space-y-3"
      >
        <button
          class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
        >
          <span>Connexion / Inscription</span>
          <Icon name="uil:user" size="20" />
        </button>
        <button
          class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
        >
          <span>Mode sombre</span>
          <Icon name="uil:moon" size="20" />
        </button>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const isOpen = ref(false);
const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});
onBeforeUnmount(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
.slide-enter-from {
  transform: translateY(-8px);
  opacity: 0;
}
.slide-enter-to {
  transform: translateY(0);
  opacity: 1;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.25s ease;
}
.slide-leave-from {
  transform: translateY(0);
  opacity: 1;
}
.slide-leave-to {
  transform: translateY(-8px);
  opacity: 0;
}
</style>
