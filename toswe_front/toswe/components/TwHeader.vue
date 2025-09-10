<template>
  <header
    :class="[
      'fixed top-0 left-0 w-full z-[1000] text-white shadow-md backdrop-blur-md transition-all duration-300',
      isScrolled ? 'bg-[rgba(107,31,13,0.8)] py-2' : 'bg-[rgba(125,38,15,0.6)] py-4'
    ]"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center">
        
        <!-- Logo -->
        <div class="flex items-center space-x-3 hover:cursor-pointer" @click="goToMarket">
          <img src="/assets/images/logo.png" alt="Tôswè" class="h-8 w-auto" />
          <span class="font-bold text-xl font-[Kumbh_Sans] tracking-wide">Tôswè</span>
          <div class="flex flex-col text-xs">
            <span v-if="auth.isAuthenticated" class="text-sm flex items-center gap-1 font-semibold">
              <span class="bg-green-500 w-2 h-2 inline-block rounded-full"></span>{{ auth.getUsername }}
            </span>
            <span class="text-xs text-gray-500 flex items-center gap-1" v-if="auth.isSeller"> <Icon name="uil:shopping-cart" size="16" /> Vendeur</span>
          </div>
        </div>

        <!-- Menu desktop -->
        <nav class="hidden md:flex items-center space-x-6 text-base">
          <!-- Si pas connecté -->
          <template v-if="!auth.isAuthenticated">
            <button
              :class="[
                'flex items-center gap-2 px-3 py-2 rounded-md transition',
                isActive('/auth') ? 'bg-white/20 text-yellow-300' : 'hover:bg-white/10'
              ]"
              @click="goToAuth"
            >
              <span class="font-[Kumbh_Sans]">Connexion / Inscription</span>
              <Icon name="uil:user" size="20" />
            </button>
            <button
              :class="[
                'flex items-center gap-2 p-2 rounded-full transition',
                isActive('/search') ? 'bg-white/20 text-yellow-300' : 'hover:bg-white/10'
              ]"
              aria-label="Rechercher un produit"
              @click="goToSearch"
            > 
              <Icon name="mdi:image-search" size="20" /> 
            </button> 
            <button
              class="flex items-center gap-2 p-2 rounded-full hover:bg-white/10 transition"
              aria-label="Nous contacter"
              @click="contactsPopup.showPopup()"
            > 
              <Icon name="uil:envelope" size="20" /> 
            </button>
          </template>

          <!-- Si connecté -->
          <template v-else>
            <button
              :class="[
                'flex items-center gap-2 p-2 rounded-full transition',
                isActive('/search') ? 'bg-white/20 text-yellow-300' : 'hover:bg-white/10'
              ]"
              aria-label="Rechercher un produit"
              @click="goToSearch"
            >
              <Icon name="mdi:image-search" size="20" />
            </button>

            <button
              :class="[
                'flex items-center gap-2 p-2 rounded-full transition',
                isActive('/orders') ? 'bg-white/20 text-yellow-300' : 'hover:bg-white/10'
              ]"
              aria-label="Commandes"
              @click="goToOrders"
            >
              <Icon name="uil:shopping-bag" size="20" />
            </button>

            <button
              :class="[
                'flex items-center gap-2 p-2 rounded-full transition',
                isActive('/notifications') ? 'bg-white/20 text-yellow-300' : 'hover:bg-white/10'
              ]"
              aria-label="Notifications"
              @click="goToNotifications"
            >
              <Icon name="uil:bell" size="20" />
            </button>

            <button
              :class="[
                'flex items-center gap-2 p-2 rounded-full transition',
                isActive('/settings') ? 'bg-white/20 text-yellow-300' : 'hover:bg-white/10'
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
                  'flex items-center gap-2 p-2 rounded-full transition',
                  isActive('/myshop') ? 'bg-white/20 text-yellow-300' : 'hover:bg-white/10'
                ]"
                aria-label="Voir ma boutique"
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
          class="md:hidden p-2 rounded-md hover:bg-white/10 transition"
          aria-label="Menu mobile"
        >
          <Icon :name="isOpen ? 'uil:times' : 'uil:bars'" size="26" />
        </button>
      </div>
    </div>

    <!-- Menu mobile -->
    <transition name="slide"> 
      <div v-if="isOpen" class="md:hidden bg-[#7D260F]/90 backdrop-blur-lg shadow-md flex flex-col items-start p-4 space-y-3" > 
        
        <!-- Si pas connecté --> 
         <template v-if="!auth.isAuthenticated"> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" @click="goToAuth" > 
            <span>Connexion / Inscription</span> <Icon name="uil:user" size="20" /> 
          </button> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" aria-label="Rechercher un produit" @click="goToSearch" > <span>Rechercher/Scanner un produit</span> <Icon name="mdi:image-search" size="20" /> </button> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" aria-label="Nous contacter" @click="contactsPopup.showPopup()" > <span>Nous contacter</span> <Icon name="uil:envelope" size="20" /> </button> 
        </template> 
        
        <!-- Si connecté --> 
         <template v-else> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" @click="goToSearch" > 
            <span>Rechercher / Scanner un produit</span> <Icon name="mdi:image-search" size="20" /> 
          </button> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" @click="goToOrders" > 
            <span>Mes commandes</span> <Icon name="uil:shopping-bag" size="20" /> 
          </button> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" @click="goToNotifications" > <span>Notifications</span> <Icon name="uil:bell" size="20" /> </button> 
          <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" @click="goToSettings" > <span>Paramètres</span> <Icon name="uil:cog" size="20" /> </button> <!-- Si vendeur --> 
          <template v-if="auth.isSeller"> 
            <button class="flex items-center gap-2 w-full px-3 py-2 rounded-md hover:bg-white/10 transition" @click="goToMyShop" > <span>Ma boutique</span> <Icon name="uil:store" size="20" /> </button> 
          </template> 
        </template> 
      </div> 
    </transition>
  </header>

  <div class="mb-17"></div>
  <TwPopupContacts ref="contactsPopup" />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useAuthStore } from '@/stores/auth'
import { goToAuth, goToNotifications, goToOrders, goToSettings, goToSearch, goToMyShop, goToMarket } from "@/utils/navigations";
import { useRoute } from "vue-router";

const auth = useAuthStore()
const contactsPopup = ref(null)
const isOpen = ref(false);
const isScrolled = ref(false);

const route = useRoute()
const isActive = (path) => route.path.startsWith(path)

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
