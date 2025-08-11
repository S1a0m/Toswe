<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative animate-fadeIn">
      <!-- Bouton Fermer -->
      <button
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        @click="close"
      >
        ✕
      </button>

      <!-- Titre -->
      <h2 class="text-xl font-semibold text-gray-800 mb-4">
        {{ isPremium ? "Devenir vendeur premium" : "Procéder au paiement" }}
      </h2>

      <!-- Description -->
      <p class="text-gray-600 text-sm mb-6">
        {{ isPremium
          ? "Le paiement pour devenir vendeur premium se fait uniquement via Mobile Money."
          : "Choisissez votre mode de paiement ci-dessous." }}
      </p>

      <!-- Sélecteur méthode de paiement -->
      <div v-if="!isPremium" class="space-y-3 mb-6">
        <label class="block border rounded-lg p-4 cursor-pointer hover:bg-gray-50">
          <input type="radio" value="momo" v-model="paymentMethod" class="mr-2" />
          Mobile Money
        </label>
        <label class="block border rounded-lg p-4 cursor-pointer hover:bg-gray-50">
          <input type="radio" value="cash" v-model="paymentMethod" class="mr-2" />
          Paiement physique (à la livraison)
        </label>
      </div>

      <!-- Si Premium → momo direct -->
      <div v-if="isPremium" class="mb-6">
        <label class="block border rounded-lg p-4 cursor-pointer hover:bg-gray-50">
          <input type="radio" value="momo" v-model="paymentMethod" checked disabled class="mr-2" />
          Mobile Money (obligatoire)
        </label>
      </div>

      <!-- Formulaire Mobile Money -->
      <div v-if="paymentMethod === 'momo'" class="mb-6">
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

<script>
export default {
  name: "TwPaymentPopup",
  props: {
    visible: { type: Boolean, default: false },
    isPremium: { type: Boolean, default: false }, // true = paiement premium, false = produit
  },
  data() {
    return {
      paymentMethod: this.isPremium ? "momo" : null,
      momoNumber: "",
    };
  },
  methods: {
    close() {
      this.$emit("close");
    },
    confirmPayment() {
      if (this.paymentMethod === "momo" && !this.momoNumber) {
        alert("Veuillez entrer votre numéro Mobile Money.");
        return;
      }
      this.$emit("pay", {
        method: this.paymentMethod,
        momoNumber: this.paymentMethod === "momo" ? this.momoNumber : null,
      });
    },
  },
};
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
