<template>
  <div class="min-h-screen bg-[#fdf8f5]">
    <ShopHeader v-if="shop" :shop="shop" :is-owner="true" />

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
              <button
                class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition"
                @click="openCreateProduct()"
              >
                + Nouveau produit
              </button>
            </div>

            <div
              v-if="products?.length"
              class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
            >
              <ShopProductCard v-for="p in products" :key="p.id" :product="p" />
            </div>
            <div
              v-else
              class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-600"
            >
              Vous n’avez pas encore de produits.
            </div>
          </div>

          <!-- Pubs -->
          <div v-else-if="active === 'ads'">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-semibold text-lg">Mes publicités</h3>
              <button
                @click="goToAdCreate"
                class="px-4 py-2 rounded-xl bg-[#7D260F] text-white hover:bg-[#66200d] transition"
              >
                + Créer une pub
              </button>
            </div>

            <div v-if="ads?.length" class="grid md:grid-cols-3 gap-4">
              <article
                v-for="a in ads"
                :key="a.id"
                class="rounded-2xl border border-[#e6d9d3] bg-white/70 shadow-sm overflow-hidden"
              >
                <div class="aspect-[16/9] bg-gray-50">
                  <img
                    :src="a.image_url || '/placeholder-banner.png'"
                    class="size-full object-cover"
                  />
                </div>
                <div class="p-4">
                  <h4 class="text-sm font-medium truncate text-[#7D260F]">
                    {{ a.title }}
                  </h4>
                  <p class="text-xs text-gray-600 line-clamp-2 mt-1">
                    {{ a.description }}
                  </p>
                </div>
              </article>
            </div>
            <div
              v-else
              class="rounded-2xl border border-[#e6d9d3] bg-white/70 p-10 text-center text-gray-600"
            >
              Aucune pub active.
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
            <form
              class="grid gap-4 max-w-xl"
              @submit.prevent="saveSettings"
            >
              <div>
                <label class="block text-sm font-medium mb-1">Nom de la boutique</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white/70"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Slogan</label>
                <input
                  v-model="form.slogan"
                  type="text"
                  class="w-full rounded-xl border border-[#e6d9d3] px-3 py-2 bg-white/70"
                />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">À propos</label>
                <textarea
                  v-model="form.about"
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

    <TwMenuSide />
  </div>
</template>


<script setup>
import { useAuthStore } from '@/stores/auth'

const tabs = [
  { key: 'products', label: 'Produits' },
  { key: 'ads', label: 'Pubs' },
  { key: 'loycs', label: 'Abonnés' },
  { key: 'settings', label: 'Paramètres' },
]
const active = ref('products')

const auth = useAuthStore()

/*/ Récupérer la boutique du vendeur connecté
const { data, pending, error } = await useFetch('/api/my-shop', {
  // baseURL: 'http://127.0.0.1:8000',
  credentials: 'include',
  headers: auth.accessToken ? { Authorization: `Bearer ${auth.accessToken}` } : {}
})*/

const data = ref({
  "shop": { "id": 1, "name": "Meubles Sam", "slogan": "La marque des boss", "about": "Nous sommes une boutique en ligne spécialisée", "logo_url": "/public/images/yonapp.png" },
  "stats": { "sales_30d": 23, "revenue_30d": 450000, "loycs": 32, "products_active": 12 },
  "products": [ 'orange', 'viandes' ],
  "ads": [ '3' ],
  "loycs": [ { "id": 2, "username": "Koffi", "orders_count": 5 } ]
})


const shop = computed(() => data.value?.shop || null)
const stats = computed(() => data.value?.stats || {})
const products = computed(() => data.value?.products || [])
const ads = computed(() => data.value?.ads || [])
const loycs = computed(() => data.value?.loycs || [])

const form = reactive({
  name: shop.value?.name || '',
  slogan: shop.value?.slogan || '',
  about: shop.value?.about || ''
})

watch(shop, (s) => {
  if (!s) return
  form.name = s.name || ''
  form.slogan = s.slogan || ''
  form.about = s.about || ''
}, { immediate: true })

const logoFile = ref(null)
const logoPreview = ref(null)
function onLogo(e) {
  const f = e.target.files?.[0]
  if (!f) return
  logoFile.value = f
  const reader = new FileReader()
  reader.onload = () => { logoPreview.value = reader.result }
  reader.readAsDataURL(f)
}

async function saveSettings() {
  const body = new FormData()
  body.append('name', form.name || '')
  body.append('slogan', form.slogan || '')
  body.append('about', form.about || '')
  if (logoFile.value) body.append('logo', logoFile.value)

  await $fetch('/api/my-shop', {
    method: 'POST',
    body,
    // baseURL: 'http://127.0.0.1:8000',
    credentials: 'include',
    headers: auth.accessToken ? { Authorization: `Bearer ${auth.accessToken}` } : {}
  })
  // TODO: toast succès + revalidate
}

function money(v) {
  if (v == null) return '—'
  try { return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'XOF' }).format(v) }
  catch { return `${v} FCFA` }
}

function openCreateProduct() { /* ouvre le modal de création */ }
</script>
