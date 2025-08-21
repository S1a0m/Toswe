<template>
  <section class="w-full space-y-8">
    <TwAdsFilter />
    <!-- Section Publicités -->
    <div class="bg-white/5 rounded-2xl shadow p-6">
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="i in 2"
          :key="'ad-' + i"
          class="bg-white/10 rounded-xl p-4 flex flex-col justify-between shadow-md hover:shadow-lg transition"
        >
          <!-- Aperçu pub -->
          <div class="aspect-video bg-gray-600 rounded-lg mb-3 flex items-center justify-center text-gray-300">
            Bannière pub
          </div>

          <!-- Infos -->
          <h3 class="text-base font-medium text-gray">Titre pub</h3>
          <p class="text-sm text-gray-400 mb-3">Texte ou résumé de la publicité…</p>

          <!-- Actions -->
          <div class="flex justify-between items-center gap-2 mt-auto">
            <button class="px-3 py-1 text-sm rounded-lg bg-[#7D260F] text-white hover:bg-[#9c3416]">
              Voir
            </button>
            <div class="flex gap-2">
              <button class="px-3 py-1 text-sm rounded-lg bg-white/20 text-gray hover:bg-white/30">
                Modifier
              </button>
              <button class="px-3 py-1 text-sm rounded-lg bg-red-600/70 text-white hover:bg-red-600">
                Supprimer
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
/**
 * Composant PendingValidations
 * - Affiche deux sections distinctes :
 *   1. Produits en attente
 *   2. Publicités en attente
 * - Chaque carte contient :
 *   - Aperçu visuel
 *   - Nom/Titre + description
 *   - Boutons d’action (Voir, Modifier, Supprimer)
 *
 * TODO : Remplacer les v-for mock par des props ou données réelles.
 */
</script>
