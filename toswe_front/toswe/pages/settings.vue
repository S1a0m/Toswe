<template>
  <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Paramètres
    </h2>

    <!-- Compte -->
    <div class="mb-8">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Compte </h2>
      <TwSettingsItem icon="uil:user" label="Profil" @click="profilPopup.showPopup()"/>
      <TwSettingsItem icon="uil:check-circle" label="Vérifier votre compte"  v-if="!auth.isVerified && auth.isSeller" @click="verifyPopup.showPopup()"/>
      <TwSettingsItem icon="uil:signout" label="Se déconnecter" @click="auth.logout"/>
      <TwSettingsItem icon="uil:trash" label="Supprimer le compte" @click="deleteAccount" danger />
    </div>

    <!-- Vente -->
    <div class="mb-8" v-if="(!auth.isSeller && !auth.isDeliverer) || (auth.isSeller && !auth.isPremiumSeller)">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Vente</h2>
      <TwSettingsItem icon="uil:briefcase" label="Devenir vendeur" v-if="!auth.isSeller && !auth.isDeliverer" @click="becomeSellerPopup.showPopup()"/>
      <TwSettingsItem icon="uil:truck" label="Devenir livreur" v-if="!auth.isDeliverer && auth.isSeller" @click="becomeDelivererPopup.showPopup()"/>
      <TwSettingsItem icon="uil:star" label="Devenir vendeur premium" v-if="auth.isSeller && !auth.isPremiumSeller" @click="goToPremium"/>
      <!--<TwSettingsItem icon="uil:chart" label="Voir mes statistiques vendeur" v-if="auth.isPremiumSeller" @click="goToStats"/>-->
    </div>

    <!-- Publicité -->
    <div class="mb-8" v-if="auth.isPremiumSeller">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Publicité</h2>
      <TwSettingsItem icon="uil:megaphone" label="Créer une campagne publicitaire" @click="goToAdCreate"/>
      <!--<TwSettingsItem icon="uil:chart" label="Voir mes performances publicitaires" @click="goToPerformances"/>-->
    </div>

    <!-- Préférences -->
    <div v-if="auth.isSeller">
      <h2 class="text-lg font-semibold text-gray-600 mb-3">Préférences</h2>
      <!--<TwSettingsItem icon="uil:shopping-cart" label="Préférences produits" @click="preferencesPopup.showPopup()"/>-->
      <TwSettingsToggle
        v-if="auth.isSeller"
        icon="uil:lock"
        label="Je suis une marque."
        v-model="isBrand"
      />
      <TwSettingsItem v-if="auth.isSeller" icon="uil:share-alt" label="Partager le lien de ma boutique" @click="copyShopLink"/>
    </div>
  </section>
  <TwPopupProfil ref="profilPopup" />
  <TwPopupVerifyAccount ref="verifyPopup" />
  <TwPopupBecomeSeller ref="becomeSellerPopup" />
  <TwPopupPreferences ref="preferencesPopup" />
</template>

<script setup>
import { goToStats, goToAdCreate } from '@/utils/navigations'
import { useAuthStore } from '@/stores/auth'
import { ref, watch } from "vue"

const auth = useAuthStore()
const isBrand = ref(auth.isBrand) // synchro locale

const profilPopup = ref(null)
const verifyPopup = ref(null)
const becomeSellerPopup = ref(null)
const becomeDelivererPopup = ref(null)
const preferencesPopup = ref(null)

watch(isBrand, async (newValue, oldValue) => {
  try {
    const response = await $fetch("http://127.0.0.1:8000/api/seller/become_brand/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })

    // Mise à jour store auth si succès
    auth.isBrand = response.seller_is_brand
    isBrand.value = response.seller_is_brand
  } catch (error) {
    console.error("Erreur API become_brand :", error)

    // rollback si erreur
    isBrand.value = oldValue
  }
})

async function copyShopLink() {
  try {
    // Ici tu copies l'URL courante (celle du navigateur)
    const shopUrl = `${window.location.origin}/shop?id=${auth.user.shop_id}`
    await navigator.clipboard.writeText(shopUrl)

    alert("✅ Lien copié dans le presse-papier !")
  } catch (err) {
    console.error("Erreur lors de la copie :", err)
    alert("❌ Impossible de copier le lien.")
  }
}

async function deleteAccount() {
  if (!confirm("❌ Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.")) {
    return
  }

  try {
    await $fetch("http://127.0.0.1:8000/api/user/delete-account/", {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })

    alert("✅ Compte supprimé avec succès.")
    auth.logout() // Déconnexion locale du store
  } catch (error) {
    console.error("Erreur suppression compte:", error)
    alert("❌ Une erreur est survenue lors de la suppression du compte.")
  }
}
</script>