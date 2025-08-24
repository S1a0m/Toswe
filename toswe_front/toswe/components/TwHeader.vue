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
        <div class="flex items-center space-x-3 hover:cursor-pointer" @click="goToMarket">
          <img src="/assets/images/logo.png" alt="Tôswè" class="h-8 w-auto" />
          <span class="font-bold text-xl font-[Kumbh_Sans] tracking-wide">Tôswè</span>
        </div>

        <!-- Menu desktop -->
        <nav class="hidden md:flex items-center space-x-6 text-base">
          <!-- Si pas connecté -->
          <template v-if="!auth.isAuthenticated">
            <button
              class="flex items-center gap-2 px-3 py-2 rounded-md hover:bg-white/10 transition"
              @click="goToAuth"
            >
              <span class="font-[Kumbh_Sans]">Connexion / Inscription</span>
              <Icon name="uil:user" size="20" />
            </button>
            <button class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition" aria-label="Rechercher un produit" @click="goToSearch" > 
              <Icon name="mdi:image-search" size="20" /> 
            </button> 
            <button class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition" aria-label="Nous contacter" @click="contactsPopup.showPopup()" > 
              <Icon name="uil:envelope" size="20" /> 
            </button>
          </template>

          <!-- Si connecté -->
          <template v-else>
            <button
              class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition"
              aria-label="Rechercher un produit"
              @click="goToSearch"
            >
              <Icon name="mdi:image-search" size="20" />
            </button>

            <button
              class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition"
              aria-label="Commandes"
              @click="goToOrders"
            >
              <Icon name="uil:shopping-bag" size="20" />
            </button>

            <button
              class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition"
              aria-label="Notifications"
              @click="goToNotifications"
            >
              <Icon name="uil:bell" size="20" />
            </button>

            <button
              class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition"
              aria-label="Paramètres"
              @click="goToSettings"
            >
              <Icon name="uil:cog" size="20" />
            </button>

            <!-- Si vendeur -->
            <template v-if="auth.isSeller">
              <button
                class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition"
                aria-label="Voir ma boutique"
                @click="goToShop"
              >
                <Icon name="uil:store" size="20" />
              </button>
            </template>
          </template>
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
        <!-- Si pas connecté -->
        <template v-if="!auth.isAuthenticated">
          <button
            class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
            @click="goToAuth"
          >
            <span>Connexion / Inscription</span>
            <Icon name="uil:user" size="20" />
          </button>
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" aria-label="Rechercher un produit" @click="goToSearch" > 
            <span>Rechercher/Scanner un produit</span> 
            <Icon name="mdi:image-search" size="20" /> 
          </button> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" aria-label="Nous contacter" @click="contactsPopup.showPopup()" > 
            <span>Nous contacter</span> 
            <Icon name="uil:envelope" size="20" /> 
          </button>
        </template>

        <!-- Si connecté -->
        <template v-else>
          <button
            class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
            @click="goToSearch"
          >
            <span>Rechercher / Scanner un produit</span>
            <Icon name="mdi:image-search" size="20" />
          </button>

          <button
            class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
            @click="goToOrders"
          >
            <span>Mes commandes</span>
            <Icon name="uil:shopping-bag" size="20" />
          </button>

          <button
            class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
            @click="goToNotifications"
          >
            <span>Notifications</span>
            <Icon name="uil:bell" size="20" />
          </button>

          <button
            class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
            @click="goToSettings"
          >
            <span>Paramètres</span>
            <Icon name="uil:cog" size="20" />
          </button>

          <!-- Si vendeur -->
          <template v-if="auth.isSeller">
            <button
              class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
              @click="goToShop"
            >
              <span>Ma boutique</span>
              <Icon name="uil:store" size="20" />
            </button>
          </template>
        </template>
      </div>
    </transition>
  </header>

  <div class="mb-18"></div>
  <TwPopupContacts ref="contactsPopup" />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useAuthStore } from '@/stores/auth'
import { goToAuth, goToNotifications, goToShop, goToSettings, goToSearch } from "@/utils/navigations";

const auth = useAuthStore()

const contactsPopup = ref(null)
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
