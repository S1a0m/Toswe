<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">📊 Performances publicitaires</h1>
      <TwPerformanceTable :data="data" />

    <!--<div v-if="pending" class="text-gray-500">Chargement...</div>
    <div v-else-if="error" class="text-red-500">Erreur: {{ error.message }}</div>
    <div v-else>
      </div>-->
    
  </div>
</template>

<script setup lang="ts">

const data = [
    {
      campaign: "Campagne Facebook",
      impressions: 12000,
      clicks: 340,
      ctr: 2.8,
      conversions: 45,
      cost: 120.5,
    },
    {
      campaign: "Google Ads",
      impressions: 25000,
      clicks: 650,
      ctr: 2.6,
      conversions: 90,
      cost: 350.75,
    },
    {
      campaign: "Instagram",
      impressions: 8000,
      clicks: 210,
      ctr: 2.62,
      conversions: 30,
      cost: 95.0,
    },
  ]
</script>
