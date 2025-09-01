<template>
  <div v-if="visible" class="fixed inset-0 z-500 flex items-center justify-center bg-black/50">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative animate-fadeIn">
      <!-- Bouton Fermer -->
      <button
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        @click="close"
      >
        ✕
      </button>

      <!-- Titre dynamique -->
      <h2 class="text-xl font-semibold text-gray-800 mb-4">
        {{ popupTitle }}
      </h2>

      <!-- Description dynamique -->
      <p class="text-gray-600 text-sm mb-6">
        {{ popupDescription }}
      </p>

      <!-- Sélecteur méthode de paiement -->
      <div v-if="requiresMethodChoice" class="space-y-3 mb-6">
        <label class="block border rounded-lg p-4 cursor-pointer hover:bg-gray-50">
          <input type="radio" value="mtn_momo" v-model="paymentMethod" class="mr-2" />
          MTN Mobile Money
        </label>
        <label class="block border rounded-lg p-4 cursor-pointer hover:bg-gray-50">
          <input type="radio" value="moov_money" v-model="paymentMethod" class="mr-2" />
          Moov Money
        </label>
      </div>

      <!-- Premium = momo obligatoire -->
      <div v-if="paymentType === 'premium'" class="mb-6">
        <label class="block border rounded-lg p-4 bg-gray-50 cursor-not-allowed">
          <input type="radio" value="mtn_momo" v-model="paymentMethod" checked disabled class="mr-2" />
          Mobile Money (obligatoire)
        </label>
      </div>

      <!-- Formulaire Mobile Money -->
      <div v-if="paymentMethod?.includes('momo')" class="mb-6">
        <label class="block text-sm font-medium mb-1">Numéro Mobile Money</label>
        <input
          v-model="momoNumber"
          type="tel"
          placeholder="Ex: 229 95 12 34 56"
          class="w-full border rounded-lg px-4 py-2 focus:ring focus:ring-blue-200"
        />
      </div>

      <!-- Bouton Valider -->
      <button
        @click="confirmPayment"
        class="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition"
      >
        Confirmer et Payer
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"

const props = defineProps({
  visible: { type: Boolean, default: false },
  paymentType: { type: String, required: true } 
  // "order" | "premium" | "sponsorship" | "advertisement"
})

const emit = defineEmits(["close", "pay"])

const paymentMethod = ref(props.paymentType === "premium" ? "mtn_momo" : null)
const momoNumber = ref("")

// Titre et description dynamiques
const popupTitle = computed(() => {
  switch (props.paymentType) {
    case "order": return "Paiement de commande"
    case "premium": return "Devenir vendeur premium"
    case "sponsorship": return "Sponsoriser un produit"
    case "advertisement": return "Créer une publicité"
    default: return "Procéder au paiement"
  }
})

const popupDescription = computed(() => {
  if (props.paymentType === "premium") {
    return "Le paiement premium se fait uniquement via Mobile Money."
  }
  return "Choisissez votre méthode de paiement."
})

const requiresMethodChoice = computed(() => props.paymentType !== "premium")

// Si le type change → reset
watch(
  () => props.paymentType,
  (val) => {
    paymentMethod.value = val === "premium" ? "mtn_momo" : null
    momoNumber.value = ""
  }
)

function close() {
  emit("close")
}

function confirmPayment() {
  if (paymentMethod.value?.includes("momo") && !momoNumber.value) {
    alert("Veuillez entrer votre numéro Mobile Money.")
    return
  }
  emit("pay", {
    paymentType: props.paymentType,
    method: paymentMethod.value,
    momoNumber: paymentMethod.value?.includes("momo") ? momoNumber.value : null,
  })
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out;
}
</style>
