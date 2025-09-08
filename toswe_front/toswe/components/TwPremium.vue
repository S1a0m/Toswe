<!-- /pages/subscribe.vue -->
<template>
  <div class="min-h-screen py-16 px-4 sm:px-6 lg:px-8 ">
    <div class="max-w-6xl mx-auto">
      <!-- Titre -->
      <div class="text-center mb-16">
        <h2 class="text-3xl sm:text-4xl font-extrabold text-[#7D260F] font-[Kenia]">
          Abonnements Tôswè
        </h2>
        <p class="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
          Choisissez le plan qui vous convient le mieux pour booster vos ventes 🚀
        </p>
      </div>

      <!-- Offres -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
        
        <!-- Plan Basic -->
        <div class="relative rounded-2xl bg-white shadow-lg hover:shadow-xl transition p-8 flex flex-col border border-gray-100">
          <h3 class="text-2xl font-bold text-gray-800 mb-3">Plan Basic</h3>
          <p class="text-gray-600 mb-6">
            Pour les vendeurs simples ou les marques qui débutent.
          </p>
          <ul class="space-y-3 flex-1">
            <!-- Vendeur simple -->
            <li class="font-semibold text-gray-700">👉 Vendeur simple :</li>
            <li class="flex items-center"><span class="text-green-500 mr-2">✔</span> Jusqu’à 5 produits</li>
            <li class="flex items-center"><span class="text-green-500 mr-2">✔</span> 2 produits sponsorisés / mois</li>

            <!-- Marque -->
            <li class="font-semibold text-gray-700 mt-4">👉 Marque :</li>
            <li class="flex items-center"><span class="text-green-500 mr-2">✔</span> Jusqu’à 10 produits</li>
            <li class="flex items-center"><span class="text-green-500 mr-2">✔</span> 4 produits sponsorisés / mois</li>
            <li class="flex items-center"><span class="text-green-500 mr-2">✔</span> 1 publicité / mois</li>
            <li class="flex items-center"><span class="text-green-500 mr-2">✔</span> Statistiques de vente</li>
          </ul>
          <div class="mt-8">
            <p class="text-3xl font-extrabold text-gray-900">Gratuit</p>
          </div>
        </div>

        <!-- Plan Premium -->
        <div class="relative rounded-2xl bg-white shadow-xl border-2 border-[#7D260F] p-8 flex flex-col">
          <!-- Badge -->
          <span class="absolute -top-3 right-6 bg-[#7D260F] text-white text-xs font-semibold px-3 py-1 rounded-full shadow-md">
            Populaire
          </span>

          <h3 class="text-2xl font-bold text-gray-800 mb-3">Plan Premium</h3>
          <p class="text-gray-600 mb-6">
            Pour les vendeurs ambitieux qui veulent plus de visibilité et d’outils puissants.
          </p>
          <ul class="space-y-3 flex-1">
            <li class="flex items-center"><span class="text-[#7D260F] mr-2">✔</span> Jusqu’à 20 produits</li>
            <li class="flex items-center"><span class="text-[#7D260F] mr-2">✔</span> 10 produits sponsorisés / mois</li>
            <li class="flex items-center"><span class="text-[#7D260F] mr-2">✔</span> 4 publicités / mois</li>
            <li class="flex items-center"><span class="text-[#7D260F] mr-2">✔</span> Statistiques pubs</li>
            <li class="flex items-center"><span class="text-[#7D260F] mr-2">✔</span> Statistiques de vente avancées</li>
            <li class="flex items-center"><span class="text-[#7D260F] mr-2">✔</span> Accès à la boutique (+ de visibilité)</li>
            <li class="flex items-center"><span class="text-[#7D260F] mr-2">✔</span> Support prioritaire</li>
          </ul>
          <div class="mt-8">
            <p class="text-3xl font-extrabold text-gray-900">9 900 CFA / mois</p>
          </div>

          <!-- CTA -->
          <div class="mt-8">
            <NuxtLink
              to="/checkout"
              class="block w-full text-center bg-[#7D260F] text-white font-bold py-3 px-6 rounded-xl shadow-md hover:bg-[#7D260F]/90 transition"
            >
              Devenir Premium
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Aucune logique JS pour l'instant
</script>
