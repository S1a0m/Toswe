<template>
    <div class="mt-18">
    </div>
    <div class="pt-0.5">
    </div>
  <section class="max-w-3xl mx-auto p-6">
    <h1 class="text-2xl font-bold mb-6">Paramètres</h1>

    <!-- Compte -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Compte userracine#R</h2>
      <TwSettingsItem icon="uil:user" label="Profil" />
      <TwSettingsItem icon="uil:signout" label="Se déconnecter" />
      <TwSettingsItem icon="uil:trash" label="Supprimer le compte" danger />
    </div>

    <!-- Vente -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Vente</h2>
      <TwSettingsItem icon="uil:briefcase" label="Devenir vendeur" />
      <TwSettingsItem icon="uil:star" label="Devenir vendeur premium" />
      <TwSettingsItem icon="uil:chart" label="Voir les statistiques vendeur" />
    </div>

    <!-- Préférences -->
    <div>
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Préférences</h2>
      <TwSettingsItem icon="uil:shopping-cart" label="Préférences produits" />
      <TwSettingsItem icon="uil:lock" label="Toujours payer avant livraison" />
      <TwSettingsItem icon="uil:share-alt" label="Voir les infos partagées par Racine à Toswe" />
    </div>
  </section>
</template>

