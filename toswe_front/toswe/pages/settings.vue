<template>
  <section class="px-4 md:px-8 py-12 max-w-3xl mx-auto">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Paramètres
    </h2>

    <!-- Compte -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Compte userracine#R</h2>
      <TwSettingsItem icon="uil:user" label="Profil" />
      <TwSettingsItem icon="uil:signout" label="Se déconnecter" @click="auth.logout"/>
      <TwSettingsItem icon="uil:trash" label="Supprimer le compte" danger />
    </div>

    <!-- Vente -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Vente</h2>
      <TwSettingsItem icon="uil:briefcase" label="Devenir vendeur" v-if="!auth.isSeller"/>
      <TwSettingsItem icon="uil:star" label="Devenir vendeur premium" v-if="auth.isSeller && !auth.isPremiumSeller"/>
      <TwSettingsItem icon="uil:chart" label="Voir mes statistiques vendeur" v-if="auth.isPremiumSeller" @click="goToStats"/>
    </div>

    <!-- Publicité -->
    <div class="mb-8" v-if="auth.isPremiumSeller">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Publicité</h2>
      <TwSettingsItem icon="uil:megaphone" label="Créer une campagne publicitaire" @click="goToAdCreate"/>
      <TwSettingsItem icon="uil:chart" label="Voir mes performances publicitaires" />
    </div>

    <!-- Préférences -->
    <div>
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Préférences</h2>
      <TwSettingsItem icon="uil:shopping-cart" label="Préférences produits" />
      <TwSettingsToggle
        icon="uil:lock"
        label="Toujours payer avant livraison"
        v-model="auth.mustPayBeforeDelivery"
      />
      <TwSettingsItem icon="uil:share-alt" label="Voir les infos partagées par Racine à Toswe" />
    </div>
  </section>
</template>

<script setup>
import { goToStats, goToAdCreate } from '@/utils/navigations'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>