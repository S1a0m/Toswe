<!--<TwHeader />-->
<template>
  <header
    :class="[
      'fixed top-0 left-0 w-full z-[1000] text-white transition-all duration-500 backdrop-blur-xl',
      isScrolled ? 'bg-gradient-to-r from-[#6B1F0D]/90 to-[#7D260F]/90 py-2 shadow-lg' : 'bg-gradient-to-r from-[#7D260F]/70 to-[#6B1F0D]/70 py-4 shadow-md'
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center">
        
        <!-- Logo -->
        <div class="flex items-center space-x-3 cursor-pointer" @click="goToMarket">
          <img src="/assets/images/logo.png" alt="Tôswè" class="h-9 w-auto drop-shadow-md" />
          <span class="hidden sm:block font-bold text-xl font-[Kumbh_Sans] tracking-wide">Tôswè</span>
          <div class="flex flex-col text-xs"> <span v-if="auth.isAuthenticated" class="text-sm flex items-center gap-1 font-semibold"> <span class="bg-green-500 w-2 h-2 inline-block rounded-full"></span>{{ auth.getUsername }} </span> <span class="text-xs text-gray-500 flex items-center gap-1" v-if="auth.isSeller"> <Icon name="uil:shopping-cart" size="16" /> Vendeur</span> </div>
        </div>

        <!-- Menu desktop -->
        <nav class="hidden md:flex items-center space-x-6 text-base">
          <!-- Pas connecté -->
          <template v-if="!auth.isAuthenticated">
            <button
              :class="[
                'flex items-center gap-2 px-4 py-2 rounded-full transition relative',
                isActive('/auth') ? 'bg-white/20 text-yellow-300 shadow-inner' : 'hover:bg-white/10'
              ]"
              @click="goToAuth"
            >
              <span class="font-[Kumbh_Sans]">Connexion / Inscription</span>
              <Icon name="uil:user" size="20" />
            </button>
            <button
              :class="[
                'flex items-center gap-2 p-3 rounded-full transition hover:scale-105 focus:ring-2 focus:ring-yellow-400/50',
                isActive('/search') ? 'bg-white/20 text-yellow-300 shadow-inner' : 'hover:bg-white/10'
              ]"
              aria-label="Rechercher un produit"
              @click="goToSearch"
            >
              <Icon name="mdi:image-search" size="20" />
            </button>
            <button
              class="flex items-center gap-2 p-3 rounded-full hover:bg-white/10 hover:scale-105 transition focus:ring-2 focus:ring-yellow-400/50"
              aria-label="Nous contacter"
              @click="contactsPopup.showPopup()"
            >
              <Icon name="uil:envelope" size="20" />
            </button>
          </template>

          <!-- Connecté -->
          <template v-else>
            <button
              :class="[
                'flex items-center gap-2 p-3 rounded-full transition hover:scale-105 focus:ring-2 focus:ring-yellow-400/50',
                isActive('/search') ? 'bg-white/20 text-yellow-300 shadow-inner' : 'hover:bg-white/10'
              ]"
              aria-label="Rechercher un produit"
              @click="goToSearch"
            >
              <Icon name="mdi:image-search" size="20" />
            </button>

            <button
              :class="[
                'flex items-center gap-2 p-3 rounded-full transition hover:scale-105 focus:ring-2 focus:ring-yellow-400/50',
                isActive('/orders') ? 'bg-white/20 text-yellow-300 shadow-inner' : 'hover:bg-white/10'
              ]"
              aria-label="Commandes"
              @click="goToOrders"
            >
              <Icon name="uil:shopping-bag" size="20" />
            </button>

            <button
              :class="[
                'flex items-center gap-2 p-3 rounded-full transition hover:scale-105 focus:ring-2 focus:ring-yellow-400/50',
                isActive('/notifications') ? 'bg-white/20 text-yellow-300 shadow-inner' : 'hover:bg-white/10'
              ]"
              aria-label="Notifications"
              @click="goToNotifications"
            >
              <Icon name="uil:bell" size="20" />
            </button>

            <button
              :class="[
                'flex items-center gap-2 p-3 rounded-full transition hover:scale-105 focus:ring-2 focus:ring-yellow-400/50',
                isActive('/settings') ? 'bg-white/20 text-yellow-300 shadow-inner' : 'hover:bg-white/10'
              ]"
              aria-label="Paramètres"
              @click="goToSettings"
            >
              <Icon name="uil:cog" size="20" />
            </button>

            <!-- Si vendeur -->
            <template v-if="auth.isSeller">
              <button
                :class="[
                  'flex items-center gap-2 p-3 rounded-full transition hover:scale-105 focus:ring-2 focus:ring-yellow-400/50',
                  isActive('/shop') ? 'bg-white/20 text-yellow-300 shadow-inner' : 'hover:bg-white/10'
                ]"
                aria-label="Ma boutique"
                @click="goToMyShop"
              >
                <Icon name="uil:store" size="20" />
              </button>
            </template>
          </template>
        </nav>

        <!-- Burger mobile -->
        <button
          @click="isOpen = !isOpen"
          class="md:hidden p-2 rounded-md hover:bg-white/10 transition relative z-50"
          aria-label="Menu mobile"
        >
          <Icon :name="isOpen ? 'uil:times' : 'uil:bars'" size="28" class="transition-transform duration-500" />
        </button>
      </div>
    </div>

    <!-- Overlay mobile -->
    <transition name="fade">
      <div v-if="isOpen" class="fixed inset-0 bg-black/50 backdrop-blur-sm md:hidden z-40" @click="isOpen=false"></div>
    </transition>

    <!-- Menu mobile -->
    <transition name="slide-fade">
      <div v-if="isOpen" class="fixed top-0 right-0 w-64 h-full bg-[#7D260F]/95 backdrop-blur-lg shadow-xl flex flex-col p-6 space-y-5 z-50">
        <!-- Pas connecté -->
        <template v-if="!auth.isAuthenticated">
          <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="goToAuth">
            <Icon name="uil:user" size="20" /> Connexion / Inscription
          </button>
          <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="goToSearch">
            <Icon name="mdi:image-search" size="20" /> Rechercher / Scanner un produit
          </button>
          <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="contactsPopup.showPopup()">
            <Icon name="uil:envelope" size="20" /> Nous contacter
          </button>
        </template>

        <!-- Connecté -->
        <template v-else>
          <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="goToSearch">
            <Icon name="mdi:image-search" size="20" /> Rechercher / Scanner un produit
          </button>
          <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="goToOrders">
            <Icon name="uil:shopping-bag" size="20" /> Mes commandes
          </button>
          <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="goToNotifications">
            <Icon name="uil:bell" size="20" /> Notifications
          </button>
          <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="goToSettings">
            <Icon name="uil:cog" size="20" /> Paramètres
          </button>
          <template v-if="auth.isSeller">
            <button class="flex items-center gap-3 px-3 py-3 rounded-md hover:bg-white/10 transition" @click="goToMyShop">
              <Icon name="uil:store" size="20" /> Ma boutique
            </button>
          </template>
        </template>
      </div>
    </transition>
  </header>

  <div class="mb-19"></div>
  <TwPopupContacts ref="contactsPopup" />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useAuthStore } from '@/stores/auth'
import { goToAuth, goToNotifications, goToOrders, goToSettings, goToSearch, goToMarket } from "@/utils/navigations";
import { useRoute } from "vue-router";
import { useNavigation } from "@/composables/useNavigation";

const { goToMyShop } = useNavigation();

const auth = useAuthStore()
const contactsPopup = ref(null)
const isOpen = ref(false)
const isScrolled = ref(false)

const route = useRoute()
const isActive = (path) => route.path.startsWith(path)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener("scroll", handleScroll))
onBeforeUnmount(() => window.removeEventListener("scroll", handleScroll))
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.4s ease;
}
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
