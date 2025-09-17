<!-- components/TwPopupPayment.vue -->
<template>
  <div v-if="visible" class="fixed inset-0 z-8000 flex items-center justify-center bg-black/50">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative animate-fadeIn">
      <!-- Bouton Fermer -->
      <button
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        @click="close"
      >
        ✕
      </button>

      <!-- Titre -->
      <h2 class="text-xl font-semibold text-gray-800 mb-4">{{ popupTitle }}</h2>
      <p class="text-gray-600 text-sm mb-6">{{ popupDescription }}</p>

      <!-- 📌 Cas spécial : Commande -->
      <div v-if="paymentType === 'order'" class="space-y-4 mb-6">
        <!-- Méthode de contact -->
        <div>
          <label class="block text-sm font-medium mb-2">Méthode de contact</label>
          <div class="flex gap-4">
            <!-- WhatsApp -->
            <label
              class="flex-1 flex items-center justify-center gap-2 border rounded-lg p-3 cursor-pointer transition
                     hover:bg-green-50"
              :class="contactMethod === 'whatsapp' ? 'border-green-500 bg-green-50' : 'border-gray-300'"
            >
              <input type="radio" value="whatsapp" v-model="contactMethod" class="hidden" />
              <Icon name="mdi:whatsapp" class="text-green-500 w-6 h-6" />
              <span class="font-medium text-sm">WhatsApp</span>
            </label>

            <!-- Appel -->
            <label
              class="flex-1 flex items-center justify-center gap-2 border rounded-lg p-3 cursor-pointer transition
                     hover:bg-blue-50"
              :class="contactMethod === 'call' ? 'border-blue-500 bg-blue-50' : 'border-gray-300'"
            >
              <input type="radio" value="call" v-model="contactMethod" class="hidden" />
              <Icon name="mdi:phone" class="text-blue-500 w-6 h-6" />
              <span class="font-medium text-sm">Appel</span>
            </label>
          </div>
        </div>

        <!-- Numéro -->
        <div>
          <label class="block text-sm font-medium mb-1">Numéro de téléphone</label>
          <input
            v-model="phoneNumber"
            type="tel"
            placeholder="Ex: 229 95 12 34 56"
            class="w-full border rounded-lg px-4 py-2 focus:ring focus:ring-blue-200"
          />
        </div>

        <!-- Adresse -->
        <div>
          <label class="block text-sm font-medium mb-1">Adresse de livraison</label>
          <textarea
            v-model="address"
            placeholder="Ex: Cotonou, quartier Zongo, maison n°12"
            class="w-full border rounded-lg px-4 py-2 focus:ring focus:ring-blue-200"
          />
        </div>
      </div>

      <!-- Premium / Sponsorship / Advertisement -->
      <div v-else class="space-y-4 mb-6">
        <label class="block border rounded-lg p-4 cursor-pointer hover:bg-gray-50">
          <input type="radio" value="mtn_momo" v-model="paymentMethod" class="mr-2" />
          MTN Mobile Money
        </label>
        <label class="block border rounded-lg p-4 cursor-pointer hover:bg-gray-50">
          <input type="radio" value="moov_money" v-model="paymentMethod" class="mr-2" />
          Moov Money
        </label>

        <div v-if="paymentMethod">
          <label class="block text-sm font-medium mb-1">Numéro Mobile Money</label>
          <input
            v-model="momoNumber"
            type="tel"
            placeholder="Ex: 229 95 12 34 56"
            class="w-full border rounded-lg px-4 py-2 focus:ring focus:ring-blue-200"
          />
        </div>
      </div>

      <!-- Bouton -->
      <button
        @click="confirmPayment"
        class="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition"
      >
        {{ paymentType === 'order' ? "Confirmer la commande" : "Confirmer et Payer" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"

const props = defineProps({
  visible: { type: Boolean, default: false },
  paymentType: { type: String, required: true }
})

const emit = defineEmits(["close", "pay"])

const contactMethod = ref(null) // whatsapp | call
const phoneNumber = ref("")
const address = ref("")
const paymentMethod = ref(null) // pour premium/sponsorship/advertisement
const momoNumber = ref("")

// Titres dynamiques
const popupTitle = computed(() => {
  switch (props.paymentType) {
    case "order": return "Confirmation de commande"
    case "premium": return "Devenir vendeur premium"
    case "sponsorship": return "Sponsoriser un produit"
    case "advertisement": return "Créer une publicité"
    default: return "Procéder au paiement"
  }
})

const popupDescription = computed(() => {
  if (props.paymentType === "premium") return "Le paiement premium se fait uniquement via Mobile Money."
  if (props.paymentType === "order") return "Veuillez entrer vos coordonnées pour organiser la livraison. Le paiement se fera à la livraison."
  return "Choisissez votre méthode de paiement."
})

// Reset si changement
watch(
  () => props.paymentType,
  () => {
    contactMethod.value = null
    phoneNumber.value = ""
    address.value = ""
    paymentMethod.value = null
    momoNumber.value = ""
  }
)

function close() {
  emit("close")
}

function confirmPayment() {
  if (props.paymentType === "order") {
    if (!contactMethod.value || !phoneNumber.value || !address.value) {
      alert("Veuillez entrer toutes vos informations de contact et adresse.")
      return
    }
    emit("pay", {
      paymentType: "order",
      contactMethod: contactMethod.value,
      phoneNumber: phoneNumber.value,
      address: address.value,
    })
    return
  }

  // Premium / Sponsorship / Advertisement
  if (!paymentMethod.value || !momoNumber.value) {
    alert("Veuillez choisir un opérateur et entrer votre numéro Mobile Money.")
    return
  }
  emit("pay", {
    paymentType: props.paymentType,
    method: paymentMethod.value,
    momoNumber: momoNumber.value,
  })
}
</script>
