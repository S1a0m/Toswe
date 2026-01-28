<template>
  <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
    <!-- En-tête -->
    <header class="flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <img
          src="/images/img1.png"
          alt="Livreur"
          class="size-14 rounded-full object-cover border border-[#e6d9d3] shadow-sm"
        />
        <div>
          <h1 class="text-2xl font-bold text-[#7D260F] font-[Kenia]">
            Bonjour, Samson
          </h1>
          <p class="text-gray-600 text-sm">Livreur agréé Tôswè</p>
        </div>
      </div>
      <button
        class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition"
      >
        Voir mes paiements
      </button>
    </header>

    <!-- Statistiques principales -->
    <section class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="rounded-2xl border border-[#e6d9d3] bg-white/70 backdrop-blur-sm p-5 shadow-sm"
      >
        <div class="text-xs text-gray-600">{{ stat.label }}</div>
        <div class="text-2xl font-semibold mt-1 text-[#7D260F]">
          {{ stat.value }}
        </div>
      </div>
    </section>

    <!-- Livraisons en cours -->
    <section>
      <h2 class="text-lg font-semibold mb-4 text-[#7D260F] flex items-center gap-2">
        <Icon name="mdi:truck-delivery" class="text-[#7D260F]" /> Livraisons en cours
      </h2>
      <div
        v-if="ongoingDeliveries.length"
        class="grid md:grid-cols-2 gap-4"
      >
        <article
          v-for="d in ongoingDeliveries"
          :key="d.id"
          class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-5 shadow-sm flex flex-col justify-between"
        >
          <div>
            <h3 class="font-semibold text-[#7D260F]">{{ d.customer }}</h3>
            <p class="text-sm text-gray-600 mt-1">Commande #{{ d.order_id }}</p>
            <p class="text-sm text-gray-500 mt-2">📍 {{ d.address }}</p>
          </div>
          <div class="flex items-center justify-between mt-4">
            <span class="text-xs bg-yellow-50 text-yellow-700 px-2 py-1 rounded-full">
              En cours
            </span>
            <button
              class="text-sm text-[#7D260F] hover:underline"
            >
              Détails →
            </button>
          </div>
        </article>
      </div>
      <div
        v-else
        class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-600"
      >
        Aucune livraison en cours.
      </div>
    </section>

    <!-- Historique des livraisons -->
    <section>
      <h2 class="text-lg font-semibold mb-4 text-[#7D260F] flex items-center gap-2">
        <Icon name="mdi:history" class="text-[#7D260F]" /> Historique récent
      </h2>
      <div
        v-if="pastDeliveries.length"
        class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-5 shadow-sm divide-y divide-[#e6d9d3]"
      >
        <div
          v-for="d in pastDeliveries"
          :key="d.id"
          class="py-3 flex justify-between items-center text-sm"
        >
          <div>
            <div class="font-medium text-gray-800">
              {{ d.customer }}
            </div>
            <div class="text-gray-500">Commande #{{ d.order_id }}</div>
          </div>
          <div class="text-right">
            <div class="text-green-600 font-medium">+{{ d.earned }} FCFA</div>
            <div class="text-xs text-gray-500">{{ d.date }}</div>
          </div>
        </div>
      </div>
      <div
        v-else
        class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-600"
      >
        Aucune livraison terminée récemment.
      </div>
    </section>
  </main>
</template>

<script setup>
import { Icon } from '@iconify/vue'

const stats = [
  { label: 'Livraisons (7j)', value: 18 },
  { label: 'Clients servis', value: 42 },
  { label: 'Revenus (30j)', value: '145 000 FCFA' },
  { label: 'Taux de satisfaction', value: '96%' },
]

const ongoingDeliveries = [
  { id: 1, order_id: 'A102', customer: 'Adjahoun Fabrice', address: 'Fidjrossè, Cotonou' },
  { id: 2, order_id: 'A103', customer: 'Kpèdjo Mireille', address: 'Akpakpa, Cotonou' },
]

const pastDeliveries = [
  { id: 1, order_id: 'A099', customer: 'Gnonlonfoun Pascal', earned: 2500, date: '05 Oct 2025' },
  { id: 2, order_id: 'A098', customer: 'Agossou Dorine', earned: 1800, date: '04 Oct 2025' },
  { id: 3, order_id: 'A097', customer: 'Adjovi Thomas', earned: 2000, date: '03 Oct 2025' },
]
</script>

<style scoped>
main {
  font-family: 'Inter', sans-serif;
}
</style>
