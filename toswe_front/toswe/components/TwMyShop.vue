<!-- TwMyShop.vue -->
<template>
  <main class="max-w-6xl mx-auto px-4 py-8 grid gap-8 lg:grid-cols-12">
    <!-- Stats -->
    <section class="lg:col-span-12 grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="s in [
          { label: 'Ventes (30j)', value: stats.sales_30d ?? '—' },
          { label: 'Revenus (30j)', value: money(stats.revenue_30d) },
          { label: 'Abonnés', value: stats.loycs ?? 0 },
          { label: 'Produits actifs', value: stats.products_active ?? 0 }
        ]"
        :key="s.label"
        class="rounded-2xl border border-[#e6d9d3] bg-white/70 backdrop-blur-sm p-5 shadow-sm"
      >
        <div class="text-xs text-gray-600">{{ s.label }}</div>
        <div class="text-2xl font-semibold mt-1 text-[#7D260F]">
          {{ s.value }}
        </div>
      </div>
    </section>

    <!-- Onglets -->
    <section class="lg:col-span-12">
      <div class="flex gap-2 overflow-x-auto pb-2">
        <button
          v-for="t in tabs"
          :key="t.key"
          @click="active = t.key"
          class="px-4 py-2 rounded-xl border transition"
          :class="active === t.key
            ? 'bg-[#7D260F] text-white border-[#7D260F]'
            : 'bg-white/70 border-[#e6d9d3] hover:bg-white'"
        >
          {{ t.label }}
        </button>
      </div>

      <!-- Contenu onglets -->
      <div class="mt-6">
        <!-- Produits -->
        <div v-if="active === 'products'">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-lg">Mes produits</h3>
            <p v-if="!auth.user?.is_premium && products.length >= max_products">Vous avez atteint la limite de {{ max_products }} produits.</p>
            <button
              class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition"
              @click="goToAddProduct"
              :class="{ 'opacity-50 cursor-not-allowed': !auth.user?.is_premium && products.length >= max_products }"
            >
              + Nouveau produit
            </button>
          </div>

          <div
            v-if="products?.length"
            class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
          >
            <TwProduct
              v-for="product in products"
              :key="product.id"
              :id="product.id"
              :image-src="product.main_image.image"
              :product-name="product.name"
              :description="product.short_description"
              :price="product.price"
              :rating="product.total_rating.average"
              :badge="product.status"
              :is-sponsored="product.is_sponsored"
              :seller-id="product.seller_id"
            />
          </div>
          <div
            v-else
            class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-600"
          >
            Vous n’avez pas encore de produits.
          </div>
        </div>

        <!-- Promotions -->
        <div v-else-if="active === 'promotions'">
          <!--<div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-lg">Mes promotions</h3>
          </div>-->

          <!-- Formulaire création promo -->
          <form
            class="space-y-4 rounded-2xl border border-[#e6d9d3] bg-white/70 p-6 shadow-sm max-w-lg"
            @submit.prevent="createPromotion"
          >
            <!-- Choix produit -->
            <div>
              <label class="block text-sm font-medium mb-1">Produit concerné</label>
              <select
                v-model="promoForm.productId"
                class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white"
              >
                <option disabled value="">-- Sélectionnez un produit --</option>
                <option v-for="p in props.products" :key="p.id" :value="p.id">
                  {{ p.name }} ({{ money(p.price) }})
                </option>
              </select>
            </div>

            <!-- Pourcentage réduction -->
            <div>
              <label class="block text-sm font-medium mb-1">Pourcentage de réduction (%)</label>
              <input
                v-model.number="promoForm.discount"
                type="number"
                min="1"
                max="90"
                placeholder="Ex: 20"
                class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white"
              />
            </div>

            <!-- Durée promo -->
            <div>
              <label class="block text-sm font-medium mb-1">Durée (jours)</label>
              <input
                v-model.number="promoForm.days"
                type="number"
                min="1"
                placeholder="Ex: 7"
                class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white"
              />
            </div>

            <!-- Prix calculé -->
            <div v-if="selectedProduct">
              <p class="text-gray-700">
                Prix initial : <span class="font-medium">{{ money(selectedProduct.price) }}</span>
              </p>
              <p class="text-gray-700">
                Réduction : -{{ promoForm.discount || 0 }}%
              </p>
              <p class="text-lg font-semibold text-[#7D260F]">
                Nouveau prix : {{ money(discountedPrice) }}
              </p>
            </div>

            <!-- Bouton -->
            <div class="pt-2">
              <button
                type="submit"
                class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition w-full"
              >
                Créer la promotion
              </button>
            </div>
          </form>
        </div>

        <!-- Pubs -->
        <div v-else-if="active === 'ads' && auth.user?.is_premium">

          <!-- Publicités -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-semibold text-lg">Mes publicités</h3>
              <button
                @click="goToAdCreate"
                class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition"
              >
                + Créer une pub
              </button>
            </div>

            <div v-if="adsList?.length" class="grid md:grid-cols-3 gap-4">
                <TwAdCard v-for="a in adsList" :key="a.id" :ad="a" />
            </div>

            <div
              v-else
              class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-600"
            >
              Aucune pub active.
            </div>
          </div>
        </div>

        <!-- Abonnés -->
        <div v-else-if="active === 'loycs'">
          <h3 class="font-semibold text-lg mb-4">Abonnés</h3>
          <div v-if="loycs?.length" class="grid md:grid-cols-3 gap-4">
            <article
              v-for="c in loycs"
              :key="c.id"
              class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-5 shadow-sm"
            >
              <div class="font-medium">{{ c.username || c.phone }}</div>
              <div class="text-xs text-gray-500">
                {{ c.orders_count || 0 }} commandes
              </div>
            </article>
          </div>
          <div
            v-else
            class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-600"
          >
            Pas encore d'abonnés.
          </div>
        </div>

        <!-- Paramètres -->
        <div v-else>
          <h3 class="font-semibold text-lg mb-4">Paramètres de la boutique</h3>
          <form class="grid gap-4 max-w-xl" @submit.prevent="updateUser">
            <div>
              <label class="block text-sm font-medium mb-1">Nom de la boutique</label>
              <input
                v-model="shopName"
                type="text"
                class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white/70"
              />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Slogan</label>
              <input
                v-model="slogan"
                type="text"
                class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white/70"
              />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">À propos</label>
              <textarea
                v-model="about"
                rows="4"
                class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white/70"
              ></textarea>
            </div>
            <div class="flex items-center gap-3">
              <input
                type="file"
                accept="image/*"
                @change="onLogo"
                class="block w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white/70"
              />
              <img
                v-if="logoPreview"
                :src="logoPreview"
                class="size-12 rounded-lg object-cover border border-[#e6d9d3]"
              />
            </div>
            <div class="pt-2">
              <button
                class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition"
              >
                Enregistrer
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  products: { type: Array, default: () => [] },
  promotions: { type: Array, default: () => [] },
  sellerId: { type: Number, required: true }
})

const auth = useAuthStore()
const tabs = [
  { key: 'products', label: 'Produits' },
  // { key: 'ads', label: 'Pubs' },
  { key: 'promotions', label: '+ Promotions' },
  { key: 'loycs', label: 'Abonnés' },
  { key: 'settings', label: 'Paramètres' }
]

if (auth.user?.is_premium) {
  tabs.splice(2, 0, { key: 'ads', label: 'Pubs' }) // insère après Produits
}

const active = ref('products')

// Promotions & publicités
const adsList = ref([])
async function fetchSellerAds() {
  try {
    const data = await $fetch(`http://127.0.0.1:8000/api/ad/by_seller/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth.accessToken}`,
      },
      credentials: 'include',
    })
    adsList.value = data?.results || data || []
  } catch (err) {
    console.error('Erreur chargement publicités du vendeur:', err)
  }
}

const max_products = computed(() => (auth.user?.is_premium ? 1000 : 20))

// === Gestion Promotion ===
const promoForm = reactive({
  productId: "",
  discount: 0,
  days: 0,
})

const selectedProduct = computed(() =>
  props.products.find((p) => p.id === promoForm.productId)
)

const discountedPrice = computed(() => {
  if (!selectedProduct.value) return 0
  const discount = promoForm.discount || 0
  return Math.round(selectedProduct.value.price * (1 - discount / 100))
})

async function createPromotion() {
  if (!promoForm.productId || !promoForm.discount || !promoForm.days) {
    alert("Veuillez remplir tous les champs.")
    return
  }

  try {
    const res = await $fetch("http://127.0.0.1:8000/api/promotion/", {
      method: "POST",
      body: {
        product: promoForm.productId,
        discount_percent: promoForm.discount,
        days: promoForm.days,
      },
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
    promotions.push({
      id: res.id,
      product_name: selectedProduct.value.name,
      discount: promoForm.discount,
      days: promoForm.days,
      new_price: discountedPrice.value,
    })
    promoForm.productId = ""
    promoForm.discount = 0
    promoForm.days = 0
    alert("Promotion créée avec succès ✅")
  } catch (err) {
    console.error("Erreur création promo:", err)
    alert("Impossible de créer la promotion")
  }
}

// Données simulées
const stats = ref({ sales_30d: 23, revenue_30d: 450000, loycs: 32, products_active: 12 })
async function fetchMyStats() {
  try {
    const data = await $fetch("http://127.0.0.1:8000/api/seller/my_stats/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
    stats.value = data
  } catch (err) {
    console.error("Erreur chargement stats vendeur:", err)
  }
}

const loycs = ref([])
async function fetchMyLoycs() {
  try {
    const data = await $fetch("http://127.0.0.1:8000/api/seller/my_subscribers/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    })
    loycs.value = data
  } catch (err) {
    console.error("Erreur chargement abonnés:", err)
  }
}

onMounted(() => {
  fetchSellerAds()
  fetchMyStats()
  fetchMyLoycs()
})


const form = reactive({
  name: '',
  slogan: '',
  about: ''
})

const logoFile = ref(null)
function buildLogoUrl(path) {
  if (!path) return null
  if (path.startsWith('http')) return path // déjà une URL absolue
  return `http://127.0.0.1:8000${path.startsWith('/') ? path : '/' + path}`
}

const logoPreview = ref(buildLogoUrl(auth.getLogo))

function onLogo(e) {
  const f = e.target.files?.[0]
  if (!f) {
    logoFile.value = null
    logoPreview.value = null
    return
  }
  logoFile.value = f
  const reader = new FileReader()
  reader.onload = () => {
    logoPreview.value = reader.result
  }
  reader.readAsDataURL(f)
}

const shopName = ref(auth.getShopName)
const about = ref(auth.getAbout)
const slogan = ref(auth.getSlogan)
const address = ref(auth.getAddress)
const phone = ref(auth.getPhone)
const username = ref(auth.getUsername)

const updateUser = async () => {
  await auth.updateUser(
    username.value,
    phone.value,
    address.value,
    shopName.value,
    about.value,
    slogan.value,
    logoFile.value
  )
}

async function saveSettings() {
  // TODO : requête API
}

function money(v) {
  if (v == null) return '—'
  try {
    return new Intl.NumberFormat('fr-FR').format(v) + ' fcfa'
  } catch {
    return `${v} fcfa`
  }
}
</script>
