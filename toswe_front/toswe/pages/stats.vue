<template>
  <section class="min-h-screen p-6">
    <!-- Titre -->
    <header class="mb-8 text-center" v-motion-slide-top>
      <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">Statistiques de Ventes</h2>
      <p class="text-gray-600">Aperçu de vos performances et activité récente</p>
    </header>

    <!-- Chiffres clés -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
      <div
        v-for="(item, index) in keyFigures"
        :key="item.label"
        class="rounded-lg p-4 text-center shadow text-white"
        :class="item.bg"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { delay: index * 0.15 } }"
      >
        <h2 class="text-xl font-bold">{{ item.value }}</h2>
        <p class="text-sm opacity-80">{{ item.label }}</p>
      </div>
    </div>

    <!-- Graphiques -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
      <!-- Ventes mensuelles -->
      <div
        class="bg-white rounded-lg p-4 shadow border"
        v-motion
        :initial="{ opacity: 0, scale: 0.9 }"
        :enter="{ opacity: 1, scale: 1, transition: { delay: 0.6 } }"
      >
        <h3 class="font-semibold mb-4">Ventes mensuelles</h3>
        <!--<BarChart
  v-if="monthlySalesData && monthlySalesData.labels && monthlySalesData.datasets"
  :chart-data="monthlySalesData"
/>--><BarChart />
      </div>

      <!-- Répartition par catégorie -->
      <div
        class="bg-white rounded-lg p-4 shadow border"
        v-motion
        :initial="{ opacity: 0, scale: 0.9 }"
        :enter="{ opacity: 1, scale: 1, transition: { delay: 0.8 } }"
      >
        <h3 class="font-semibold mb-4">Répartition par catégorie</h3>
        <!--<PieChart :chart-data="categoryData" />--><PieChart />
      </div>
    </div>

    <!-- Top Produits -->
    <div
      class="bg-white rounded-lg shadow border p-4"
      v-motion
      :initial="{ opacity: 0, y: 40 }"
      :enter="{ opacity: 1, y: 0, transition: { delay: 1 } }"
    >
      <h3 class="font-semibold mb-4">Top Produits</h3>
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-100 text-left text-sm">
            <th class="p-2">Produit</th>
            <th class="p-2">Ventes</th>
            <th class="p-2">Revenu</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(product, i) in topProducts"
            :key="i"
            class="border-t hover:bg-gray-50"
          >
            <td class="p-2 flex items-center gap-3">
              <img :src="product.image" alt="" class="w-10 h-10 rounded object-cover" />
              <span class="text-sm font-medium">{{ product.name }}</span>
            </td>
            <td class="p-2 text-sm">{{ product.sales }}</td>
            <td class="p-2 text-sm font-medium">{{ formatCurrency(product.revenue) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
definePageMeta({
  middleware: 'auth', // Appliquer le middleware d'authentification
})
import { ref, computed } from 'vue'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale } from 'chart.js'
import { Bar, Pie } from 'vue-chartjs'

// Enregistrement Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale)

/*const BarChart = Bar
const PieChart = Pie*/

// Données simulées
const stats = ref({
  totalSales: 352,
  totalRevenue: 1250000,
  subscribers: 134,
  avgBasket: 3550
})

const keyFigures = computed(() => [
  { label: 'Produits vendus', value: stats.value.totalSales, bg: 'bg-[#7D260F]' },
  { label: 'Revenus totaux', value: formatCurrency(stats.value.totalRevenue), bg: 'bg-green-600' },
  { label: 'Clients fidèles', value: stats.value.subscribers, bg: 'bg-blue-600' },
  { label: 'Panier moyen', value: formatCurrency(stats.value.avgBasket), bg: 'bg-yellow-500 text-black' }
])

// Graphiques
const monthlySalesData = ref({
  labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août'],
  datasets: [
    { label: 'Ventes', data: [20, 45, 32, 50, 65, 40, 80, 90], backgroundColor: '#7D260F' }
  ]
})

const categoryData = ref({
  labels: ['Mode', 'Maison', 'Beauté', 'Alimentation', 'Autres'],
  datasets: [
    {
      label: 'Répartition',
      data: [35, 20, 15, 25, 5],
      backgroundColor: ['#7D260F', '#4CAF50', '#2196F3', '#FFC107', '#9E9E9E']
    }
  ]
})

// Top produits simulés
const topProducts = ref([
  { name: 'Robe en wax', sales: 120, revenue: 480000, image: '/assets/images/img1.png' },
  { name: 'Chaussures cuir', sales: 90, revenue: 540000, image: '/assets/images/img2.jpg' },
  { name: 'Collier artisanal', sales: 75, revenue: 225000, image: '/assets/images/img3.jpg' }
])

function formatCurrency(amount) {
  return amount.toLocaleString('fr-FR', { style: 'currency', currency: 'XOF' })
}
</script>
