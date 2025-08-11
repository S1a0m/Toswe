<template>
  <Pie :data="chartData" :options="chartOptions" />
</template>

<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const chartData = {
  labels: ['Rouge', 'Bleu', 'Jaune'],
  datasets: [
    {
      label: 'Répartition',
      data: [30, 45, 25],
      backgroundColor: ['#f87171', '#60a5fa', '#facc15'],
    },
  ],
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'bottom',
    },
  },
}
</script>
