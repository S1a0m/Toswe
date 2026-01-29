<template>
  <main class="max-w-6xl mx-auto px-4 py-6 md:py-8 grid gap-6 md:gap-8 lg:grid-cols-12">
    <section class="lg:col-span-12 grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
      <div
        v-for="s in [
          { label: 'Ventes (30j)', value: stats.sales_30d ?? '—' },
          { label: 'Revenus (30j)', value: money(stats.revenue_30d) },
          { label: 'Abonnés', value: stats.loycs ?? 0 },
          { label: 'Produits actifs', value: stats.products_active ?? 0 }
        ]"
        :key="s.label"
        class="rounded-2xl border border-[#e6d9d3] bg-white/70 backdrop-blur-sm p-4 md:p-5 shadow-sm"
      >
        <div class="text-[10px] md:text-xs uppercase tracking-wider text-gray-500 font-medium">{{ s.label }}</div>
        <div class="text-lg md:text-2xl font-semibold mt-1 text-[#7D260F] truncate">
          {{ s.value }}
        </div>
      </div>
    </section>

    <section class="lg:col-span-12">
      <div class="flex gap-2 overflow-x-auto pb-2 no-scrollbar -mx-4 px-4 md:mx-0 md:px-0">
        <button
          v-for="t in tabs"
          :key="t.key"
          @click="active = t.key"
          class="px-4 py-2 rounded-xl border transition whitespace-nowrap text-sm md:text-base"
          :class="active === t.key
            ? 'bg-[#7D260F] text-white border-[#7D260F] shadow-md'
            : 'bg-white/70 border-[#e6d9d3] hover:bg-white text-gray-600'"
        >
          {{ t.label }}
        </button>
      </div>

      <div class="mt-6 md:mt-8">
        
        <div v-if="active === 'products'">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <div>
                <h3 class="font-bold text-xl text-gray-800">Mes produits</h3>
                <p v-if="!auth.user?.is_premium && products.length >= max_products" class="text-xs text-red-500 mt-1">
                    Limite de {{ max_products }} produits atteinte.
                </p>
            </div>
            <button
              class="inline-flex items-center justify-center px-5 py-2.5 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition font-medium text-sm shadow-sm"
              @click="goToAddProduct"
              :class="{ 'opacity-50 cursor-not-allowed': !auth.user?.is_premium && products.length >= max_products }"
            >
              <span class="mr-2 text-lg">+</span> Nouveau produit
            </button>
          </div>

          <div
            v-if="products?.length"
            class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-6"
          >
            <TwProduct
              v-for="product in products"
              :key="product.id"
              :id="product.id"
              :image-src="product.main_image?.image"
              :product-name="product.name"
              :description="product.short_description"
              :price="product.price"
              :rating="product.total_rating?.average"
              :badge="product.status"
              :is-sponsored="product.is_sponsored"
              :seller-id="product.seller_id"
            />
          </div>
          <div
            v-else
            class="rounded-3xl border-2 border-dashed border-[#e6d9d3] bg-white/40 p-12 text-center text-gray-500"
          >
            <p>Vous n’avez pas encore de produits.</p>
          </div>
        </div>

        <div v-else-if="active === 'promotions'">
          <div class="max-w-xl mx-auto md:mx-0">
            <h3 class="font-bold text-xl mb-6">Créer une promotion</h3>
            <form
                class="space-y-5 rounded-2xl border border-[#e6d9d3] bg-white p-5 md:p-8 shadow-sm"
                @submit.prevent="createPromotion"
            >
                <div>
                <label class="block text-sm font-semibold mb-2">Produit concerné</label>
                <select
                    v-model="promoForm.productId"
                    class="w-full rounded-xl border border-gray-200 px-4 py-3 bg-gray-50 focus:ring-2 focus:ring-[#7D260F]/20 focus:border-[#7D260F] outline-none transition"
                >
                    <option disabled value="">-- Sélectionnez un produit --</option>
                    <option v-for="p in props.products" :key="p.id" :value="p.id">
                    {{ p.name }} ({{ money(p.price) }})
                    </option>
                </select>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                    <label class="block text-sm font-semibold mb-2">Réduction (%)</label>
                    <input
                        v-model.number="promoForm.discount"
                        type="number" min="1" max="90"
                        class="w-full rounded-xl border border-gray-200 px-4 py-3 bg-gray-50 outline-none focus:border-[#7D260F]"
                    />
                    </div>
                    <div>
                    <label class="block text-sm font-semibold mb-2">Durée (jours)</label>
                    <input
                        v-model.number="promoForm.days"
                        type="number" min="1"
                        class="w-full rounded-xl border border-gray-200 px-4 py-3 bg-gray-50 outline-none focus:border-[#7D260F]"
                    />
                    </div>
                </div>

                <div v-if="selectedProduct" class="p-4 rounded-xl bg-[#7D260F]/5 border border-[#7D260F]/10">
                    <div class="flex justify-between text-sm text-gray-600 mb-1">
                        <span>Prix initial</span>
                        <span>{{ money(selectedProduct.price) }}</span>
                    </div>
                    <div class="flex justify-between text-sm text-red-600 mb-2 font-medium">
                        <span>Réduction</span>
                        <span>-{{ promoForm.discount || 0 }}%</span>
                    </div>
                    <div class="flex justify-between text-lg font-bold text-[#7D260F] pt-2 border-t border-[#7D260F]/10">
                        <span>Nouveau prix</span>
                        <span>{{ money(discountedPrice) }}</span>
                    </div>
                </div>

                <button
                    type="submit"
                    class="w-full py-4 rounded-xl bg-[#7D260F] text-white font-bold hover:bg-[#66200d] shadow-lg shadow-[#7D260F]/20 transition transform active:scale-[0.98]"
                >
                    Activer la promotion
                </button>
            </form>
          </div>
        </div>

        <div v-else-if="active === 'ads' && auth.user?.is_premium">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <h3 class="font-bold text-xl">Mes publicités</h3>
            <button
              @click="goToAdCreate"
              class="px-5 py-2.5 rounded-xl bg-[#7D260F] text-white font-medium shadow-sm"
            >
              + Créer une pub
            </button>
          </div>
          <div v-if="adsList?.length" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <TwAdCard v-for="a in adsList" :key="a.id" :ad="a" />
          </div>
          <div v-else class="rounded-3xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-500">
            Aucune publicité active.
          </div>
        </div>

        <div v-else-if="active === 'loycs'">
          <h3 class="font-bold text-xl mb-6">Mes Abonnés</h3>
          <div v-if="loycs?.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <article
              v-for="c in loycs"
              :key="c.id"
              class="flex items-center gap-4 rounded-2xl border border-[#e6d9d3] bg-white p-4 shadow-sm"
            >
              <div class="size-10 rounded-full bg-[#7D260F]/10 flex items-center justify-center text-[#7D260F] font-bold">
                {{ (c.username || 'U').charAt(0).toUpperCase() }}
              </div>
              <div>
                <div class="font-bold text-gray-800">{{ c.username || c.phone }}</div>
                <div class="text-xs text-gray-500">{{ c.orders_count || 0 }} commandes</div>
              </div>
            </article>
          </div>
          <div v-else class="rounded-3xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-500">
            Pas encore d'abonnés.
          </div>
        </div>

        <div v-else>
          <h3 class="font-bold text-xl mb-6">Paramètres Boutique</h3>
          <form class="grid gap-5 max-w-2xl" @submit.prevent="updateUser">
            <div class="grid md:grid-cols-2 gap-4">
                <div>
                <label class="block text-sm font-semibold mb-2">Nom de la boutique</label>
                <input v-model="shopName" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 bg-white outline-none focus:border-[#7D260F]" />
                </div>
                <div>
                <label class="block text-sm font-semibold mb-2">Slogan</label>
                <input v-model="slogan" type="text" class="w-full rounded-xl border border-gray-200 px-4 py-3 bg-white outline-none focus:border-[#7D260F]" />
                </div>
            </div>
            <div>
              <label class="block text-sm font-semibold mb-2">À propos</label>
              <textarea v-model="about" rows="4" class="w-full rounded-xl border border-gray-200 px-4 py-3 bg-white outline-none focus:border-[#7D260F]"></textarea>
            </div>
            
            <div class="p-4 rounded-xl border border-[#e6d9d3] bg-white/50">
                <label class="block text-sm font-semibold mb-3">Logo de la boutique</label>
                <div class="flex items-center gap-5">
                    <img
                        v-if="logoPreview"
                        :src="logoPreview"
                        class="size-20 rounded-2xl object-cover border-2 border-white shadow-md"
                    />
                    <div class="flex-1">
                        <input
                            type="file"
                            accept="image/*"
                            @change="onLogo"
                            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-[#7D260F]/10 file:text-[#7D260F] hover:file:bg-[#7D260F]/20"
                        />
                    </div>
                </div>
            </div>

            <div class="pt-4">
              <button class="w-full md:w-auto px-10 py-3.5 rounded-xl bg-[#7D260F] text-white font-bold hover:bg-[#66200d] transition shadow-lg shadow-[#7D260F]/20">
                Enregistrer les modifications
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
/* Masquer la scrollbar pour les onglets sur mobile */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

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
