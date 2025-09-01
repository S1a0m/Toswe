<template>
  <footer class="bg-[#1E1E1E] text-white text-sm py-10 px-5">
    <div
      class="max-w-7xl mx-auto flex flex-wrap justify-between gap-10 text-left"
    >
      <!-- Section Tôswè -->
      <div class="flex-1 min-w-[200px]">
        <h3 class="text-white text-lg mb-2 font-semibold">Tôswè</h3>
        <p class="text-gray-400 mb-1">
          Plateforme intelligente de vente et de livraison locale. 
        </p>
        <p class="text-gray-400">
          Ce qui n'est pas africain n'est pas Tôswè !
        </p>
      </div>

      <!-- Section Liens utiles -->
      <div class="flex-1 min-w-[200px]">
        <h4 class="text-white text-base mb-2 font-semibold">Liens utiles</h4>
        <ul class="list-none p-0 m-0 space-y-1">
          <li>
            <a href="#" class="text-gray-400 hover:underline"
              >Politique de confidentialité</a
            >
          </li>
          <li>
            <a href="#" class="text-gray-400 hover:underline"
              >Conditions d'utilisation</a
            >
          </li>
          <li>
            <a
              href="#features-section"
              class="text-gray-400 hover:underline"
              >Fonctionnalités</a
            >
          </li>
          <!--<li
              v-if="canInstall"
              @click="install">
            <a href="#telechargement" class="text-gray-400 hover:underline"
              >Télécharger</a
            >
          </li>-->
        </ul>
      </div>

      <!-- Section Suivez-nous -->
      <div class="flex-1 min-w-[200px]">
        <h4 class="text-white text-base mb-3 font-semibold">Suivez-nous</h4>
        <div class="flex space-x-4">
            <!-- Facebook -->
            <a
              href="https://facebook.com/tonpage"
              target="_blank"
              class="text-gray-400"
            >
              <Icon name="simple-icons:facebook" class="w-5 h-5" />
            </a>

            <!-- TikTok -->
            <a
              href="https://tiktok.com/@toncompte"
              target="_blank"
              class="text-gray-400"
            >
              <Icon name="simple-icons:tiktok" class="w-5 h-5" />
            </a>

            <!-- WhatsApp -->
            <a
              href="https://wa.me/tonnumero"
              target="_blank"
              class="text-gray-400"
            >
              <Icon name="simple-icons:whatsapp" class="w-5 h-5" />
            </a>
        </div>
      </div>

      <!-- Section Contact -->
      <div class="flex-1 min-w-[200px]">
        <h4 class="text-white text-base mb-3 font-semibold">Contact</h4>

        <p class="flex items-center text-gray-400 mb-1 gap-3">
          <Icon name="feather:edit" class="w-5 h-5"/>
          <a href="mailto:contact@toswe.africa" class="hover:underline"
            >contact@toswe.africa</a
          >
        </p>

        <p class="flex items-center text-gray-400 mb-1 gap-3">
          <Icon name="feather:phone" class="w-5 h-5"/>
          +229 90 00 00 00
        </p>

        <p class="flex items-center text-gray-400 gap-3">
          <Icon name="feather:map-pin" class="w-5 h-5"/>
          Abomey-Calavi, Bénin
        </p>
      </div>
    </div>

    <div class="border-t border-gray-700 mt-8 pt-4 text-center text-gray-500 text-xs">
      © 2025 Tôswè. Tous droits réservés.
    </div>
  </footer>
</template>

<script setup lang="ts">
/*import { usePwaInstall } from '@/composables/usePwaInstall'

const { canInstall, install } = usePwaInstall()*/
</script>