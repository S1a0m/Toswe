<template>
  <div
    class="bg-white border border-[#7D260F33] rounded-lg shadow-md p-4 flex items-start justify-between gap-4 max-w-md"
  >
    <!-- Contenu texte -->
    <div class="flex-1">
      <h4 class="text-lg font-bold text-[#7D260F] mb-1">Alerte commande</h4>
      <p class="text-gray-700 text-sm mb-2">
        Votre commande a été bien reçue. Vous serez livré dans quelques heures.
      </p>
      <div class="text-xs text-gray-500">
        Envoyé à <time datetime="2025-08-09T17:01">17:01</time>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex flex-col items-center gap-2">
      <Icon
        name="mdi:check"
        size="20"
        class="text-green-600 cursor-pointer hover:scale-110 transition-transform"
      />
      <Icon
        name="mdi:delete"
        size="20"
        class="text-red-500 cursor-pointer hover:scale-110 transition-transform"
      />
    </div>
  </div>
</template>
