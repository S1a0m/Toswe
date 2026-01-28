<!-- TwProduct.vue -->
<template>
  <div
    class="relative group w-full max-w-xs rounded-2xl overflow-hidden shadow-md 
           bg-white/90 backdrop-blur-lg border border-white/20 
           hover:shadow-xl hover:-translate-y-1 transition-all duration-500"
    :class="{ 'border-yellow-400 shadow-yellow-200/40': isSponsored }"
  >
    <!-- Ruban Sponsorisé -->
    <div
      v-if="isSponsored"
      class="absolute top-0 right-0 bg-gradient-to-r from-yellow-400 to-yellow-500 
             text-white text-[10px] font-bold px-2 py-1 rounded-bl-lg shadow-md uppercase tracking-wide z-10"
    >
      Sponsorisé
    </div>

    <!-- Image produit -->
    <div class="relative w-full h-48">
      <img
        :src="imageSrc"
        :alt="productName"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110 cursor-pointer"
        @click="goToProductDetails(id)"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent"></div>

      <!-- Badge -->
      <span
        v-if="badge"
        class="absolute top-3 left-3 bg-gradient-to-r from-[#7D260F] to-[#A13B20] 
               text-white text-xs font-semibold px-2 py-0.5 rounded-full shadow-md"
      >
        {{ badge }}
      </span>

    <!-- ✅ Boutons CRUD (uniquement si propriétaire) -->
    <div
      v-if="isOwner && route.path === '/shop'"
      class="absolute top-3 right-3 flex flex-col gap-2 z-20"
    >
      <button
        @click="goToProductEdit(id)"
        class="p-2 flex items-center justify-center bg-white/90 rounded-full shadow hover:bg-yellow-100 transition border border-[#e6d9d3]"
      >
        <Icon name="mdi:pencil" size="18" class="text-yellow-600" />
      </button>

      <button
        @click.stop="deleteProduct"
        class="p-2 flex items-center justify-center bg-white/90 rounded-full shadow hover:bg-red-100 transition border border-[#e6d9d3]"
      >
        <Icon name="mdi:trash-can" size="18" class="text-red-600" />
      </button>

      <!-- ✅ Bouton QR Code -->
      <button
        @click.stop="fetchQrCode"
        class="p-2 flex items-center justify-center bg-white/90 rounded-full shadow hover:bg-green-100 transition border border-[#e6d9d3]"
      >
        <Icon name="mdi:qrcode" size="18" class="text-green-600" />
      </button>

            <!--<button
            v-if="!isSponsored"
              @click="showPopup = true"
              class="p-2 flex items-center justify-center bg-white/90 rounded-full shadow hover:bg-blue-100 transition border border-[#e6d9d3]"
            >
              <Icon name="mdi:bullhorn" size="18" class="text-blue-600" />
            </button> -->
          </div>
    </div>


    <!-- Contenu -->
    <div class="absolute bottom-0 left-0 right-0 p-4 text-white 
                transition-all duration-500 group-hover:translate-y-[-10%]">
      <h3
        class="font-semibold text-base truncate cursor-pointer"
        @click="goToProductDetails(id)"
      >
        {{ productName }}
      </h3>

      <p class="text-xs opacity-90 line-clamp-2 cursor-pointer"
        @click="goToProductDetails(id)" v-html="contentSanitized"></p>

      <!-- Étoiles -->
      <div class="flex items-center gap-1 mt-1">
        <Icon
          v-for="n in 5"
          :key="n"
          name="uil:star"
          size="14"
          :class="
            n <= Math.floor(rating)
              ? 'text-yellow-400'
              : n - rating < 1
              ? 'text-yellow-300/60'
              : 'text-gray-400'
          "
        />
        <span class="text-xs opacity-80">({{ rating.toFixed(1) }})</span>
      </div>

      <!-- ✅ Prix + bouton Panier -->
      <div
        class="flex items-center justify-between mt-3 
               opacity-100 translate-y-0 
               lg:opacity-0 lg:translate-y-5 
               lg:group-hover:opacity-100 lg:group-hover:translate-y-0 
               transition-all duration-500"
      >
        <span class="text-sm font-semibold text-yellow-300">{{ price }} FCFA</span>
        <button
          v-if="!isOwner"
          class="px-3 py-1.5 bg-gradient-to-r from-[#7D260F] to-[#A13B20] 
                 text-white text-xs font-semibold rounded-lg shadow-md 
                 hover:shadow-lg hover:from-[#A13B20] hover:to-[#7D260F] 
                 transition-all duration-300 active:scale-95"
          :class="{ animate: isAnimating }"
          @click.stop="handleAddClick"
        >
          {{ isAdded ? "Panier" : "Ajouter" }}
        </button>
      </div>
    </div>
  </div>

  <!-- ✅ Popup QR Code -->
<div
  v-if="showQrPopup"
  class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
>
  <div class="bg-white rounded-2xl p-6 shadow-xl max-w-sm w-full relative">
    <button
      @click="showQrPopup = false"
      class="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
    >
      ✕
    </button>
    <h2 class="text-lg font-semibold text-center mb-4">QR Code du produit</h2>
    <img
      v-if="qrCodeUrl"
      :src="qrCodeUrl"
      alt="QR Code"
      class="w-48 h-48 mx-auto"
    />
<div class="flex gap-2 mt-4">
  <!-- Télécharger -->
  <button 
    @click="downloadQrCode"
    class="flex-1 py-2 bg-[#7D260F] text-white rounded-lg flex items-center justify-center gap-1 hover:bg-[#A13B20] transition"
  >
    Télécharger <Icon name="mdi:download" />
  </button>

  <!-- Partager -->
  <button 
    @click="shareQrCode"
    class="flex-1 py-2 bg-blue-600 text-white rounded-lg flex items-center justify-center gap-1 hover:bg-blue-700 transition"
  >
    Partager <Icon name="mdi:share-variant" />
  </button>
</div>

  </div>
</div>


    <!-- Popup paiement -->
    <TwPopupPayment
      v-if="showPopup"
      :visible="showPopup"
      payment-type="sponsorship"
      @close="showPopup = false"
      @pay="handlePayment"
    />
</template>


<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useNavigation } from '@/composables/useNavigation'
import { useRoute } from 'vue-router'

import DOMPurify from 'dompurify'

const showPopup = ref(false)

const route = useRoute()

const { goToProductDetails, goToProductEdit } = useNavigation()
const auth = useAuthStore()
const cart = useCartStore()

const props = defineProps({
  id: { type: Number, required: true },
  sellerId: { type: Number, required: true },
  imageSrc: { type: String, default: '/images/img2.jpg' },
  productName: { type: String, default: 'Nom du produit' },
  description: { type: String, default: 'Courte description du produit.' },
  price: { type: Number, default: 3000 },
  rating: { type: Number, default: 4.5 },
  badge: { type: String, default: 'Nouveau' },
  isSponsored: { type: Boolean, default: false }
})

const isOwner = computed(() => auth?.user?.id === props.sellerId)

const isAdded = ref(false)
const isAnimating = ref(false)

const product = {
  product_id: props.id,
  main_image: props.imageSrc,
  name: props.productName,
  price: props.price
}
console.log("Image princiale:", props.imageSrc)

function handleAddClick() {
  if (isAdded.value) {
    goToCart()
    return
  }
  cart.addToCart(product)
  isAdded.value = true
  isAnimating.value = true
  setTimeout(() => { isAnimating.value = false }, 300)
}

async function handlePayment(payload) {
  try {
    // payload = { paymentType: "sponsorship", paymentMethod, userNumber, sponsorDays, totalPrice }

    if (payload.paymentType === "sponsorship") {
      const body = {
        ad_type: "sponsored",
        product: props.id,           // ID du produit
        amount: payload.totalPrice,  // calculé par TwPopupPayment
      }

      const response = await $fetch("http://127.0.0.1:8000/api/ad/", {
        method: "POST",
        body,
        headers: { Authorization: `Bearer ${auth.accessToken}` }
      })

      alert("🎉 Votre produit est sponsorisé avec succès !")
    }
  } catch (error) {
    console.error("Erreur sponsorisation:", error)
    alert("❌ Une erreur est survenue. Veuillez réessayer.")
  } finally {
    showPopup.value = false
  }
}

const showQrPopup = ref(false)
const qrCodeUrl = ref(null)

// 🔹 Récupérer QR code depuis l’API
async function fetchQrCode() {
  try {
    const response = await $fetch(`http://127.0.0.1:8000/api/product/${props.id}/get_qr_code/`, {
      headers: { Authorization: `Bearer ${auth.accessToken}` }
    })
    qrCodeUrl.value = response.qr_code_url
    showQrPopup.value = true
  } catch (error) {
    console.error("Erreur QR Code:", error)
    alert("❌ Impossible de charger le QR code.")
  }
}

// Télécharger le QR Code
function downloadQrCode() {
  if (!qrCodeUrl.value) return

  const link = document.createElement("a")
  link.href = qrCodeUrl.value
  link.download = `qr_code_produit_${props.id}.png`  // nom du fichier
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Partager le QR Code
async function shareQrCode() {
  if (!qrCodeUrl.value) return

  // Si le navigateur supporte Web Share API
  if (navigator.share) {
    try {
      await navigator.share({
        title: "QR Code Produit",
        text: "Voici le QR code de mon produit sur Tôswè.",
        url: qrCodeUrl.value
      })
    } catch (err) {
      console.error("Partage annulé ou erreur :", err)
    }
  } else {
    // Fallback si share() n’est pas supporté
    alert("Le partage n’est pas supporté sur ce navigateur.")
  }
}


async function deleteProduct() {
  if (!confirm("Supprimer ce produit ?")) return

  try {
    await $fetch(`http://127.0.0.1:8000/api/product/${props.id}/delete/`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })

    alert("✅ Produit supprimé avec succès.")
    // rafraîchir la page ou émettre un event pour retirer le produit du DOM
    // Exemple :
    // emit("deleted", props.id)
  } catch (error) {
    console.error("Erreur suppression produit:", error)
    alert("❌ Impossible de supprimer ce produit.")
  }
}

const contentSanitized = ref('')

onMounted(() => {
  contentSanitized.value = DOMPurify.sanitize(props.description, {
    ALLOWED_TAGS: ['b', 'i', 'strong', 'em', 'br']
  })
})


</script>
