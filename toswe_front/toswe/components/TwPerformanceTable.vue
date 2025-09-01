<template>
  <div class="overflow-x-auto rounded-lg shadow-md">
    <table class="min-w-full border-collapse bg-white dark:bg-gray-900">
      <thead class="bg-gray-100 dark:bg-gray-800">
        <tr>
          <th class="px-4 py-2 text-left">Campagne</th>
          <th class="px-4 py-2 text-right">Impressions</th>
          <th class="px-4 py-2 text-right">Clics</th>
          <th class="px-4 py-2 text-right">CTR (%)</th>
          <th class="px-4 py-2 text-right">Conversions</th>
          <th class="px-4 py-2 text-right">Coût (€)</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, index) in data"
          :key="index"
          class="border-b hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          <td class="px-4 py-2">{{ item.campaign }}</td>
          <td class="px-4 py-2 text-right">{{ item.impressions }}</td>
          <td class="px-4 py-2 text-right">{{ item.clicks }}</td>
          <td class="px-4 py-2 text-right">{{ item.ctr }}</td>
          <td class="px-4 py-2 text-right">{{ item.conversions }}</td>
          <td class="px-4 py-2 text-right">{{ item.cost.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  data: Array<{
    campaign: string
    impressions: number
    clicks: number
    ctr: number
    conversions: number
    cost: number
  }>
}>()
</script>
