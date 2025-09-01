<template>
  <div class="min-h-screen">
    <ShopHeader
      v-if="shop"
      :shop="shop"
      :is-owner="isOwner"
      @contact="openContact()"
      @follow="toggleFollow()"
    />

    <!-- Skeleton en-tête -->
    <div v-else class="bg-white/90 backdrop-blur border-b">
      <div class="max-w-6xl mx-auto px-4 py-6 animate-pulse">
        <div class="h-10 w-1/3 bg-gray-200 rounded"></div>
        <div class="mt-3 h-4 w-1/2 bg-gray-200 rounded"></div>
      </div>
    </div>

    <main class="max-w-6xl mx-auto px-4 py-6">
      <!-- À propos -->
      <section v-if="shop?.about" class="mb-8">
        <h2 class="font-semibold text-lg mb-2">À propos</h2>
        <p class="text-gray-700 leading-relaxed" :class="{'line-clamp-3': !showMore}">
          {{ shop.about }}
        </p>
        <button
          v-if="shop.about && shop.about.length > 220"
          class="mt-2 text-sm text-[#7D260F] hover:underline"
          @click="showMore = !showMore"
        >
          {{ showMore ? 'Voir moins' : 'Voir plus' }}
        </button>
      </section>

      <!-- Publicités -->
      <section v-if="ads?.length" class="mb-8">
        <h2 class="font-semibold text-lg mb-3">Promotions</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <article
            v-for="a in ads"
            :key="a.id"
            class="rounded-xl border bg-white overflow-hidden"
          >
            <div class="aspect-[16/9] bg-gray-50">
              <img :src="a.image_url || '/placeholder-banner.png'" class="size-full object-cover" />
            </div>
            <div class="p-3">
              <h3 class="text-sm font-medium truncate">{{ a.title }}</h3>
              <p class="text-xs text-gray-600 line-clamp-2 mt-1">{{ a.description }}</p>
            </div>
          </article>
        </div>
      </section>

      <!-- Produits -->
      <section class="mb-8">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold text-lg">Produits</h2>
          <div class="text-sm text-gray-500">{{ products?.length || 0 }} résultats</div>
        </div>

        <!-- grid -->
        <div v-if="products?.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <ShopProductCard v-for="p in products" :key="p.id" :product="p" />
        </div>

        <!-- states -->
        <div v-else-if="pending" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 animate-pulse">
          <div v-for="i in 8" :key="i" class="h-56 rounded-xl bg-gray-200"></div>
        </div>
        <div v-else class="rounded-xl border bg-white p-8 text-center text-gray-600">
          Aucun produit pour le moment.
        </div>
      </section>
    </main>
    <TwMenuSide />
    <TwCart />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { mockShopData } from '@/mocks/mockShopData'

const auth = useAuthStore()
const route = useRoute()
const showMore = ref(false)

// Simulation API
const pending = ref(false)
const error = ref(null)
const data = ref(mockShopData)

const shop = computed(() => data.value?.shop)
const products = computed(() => data.value?.products || [])
const ads = computed(() => data.value?.ads || [])
const isOwner = computed(() => !!shop.value && auth?.user?.id === shop.value?.owner_id)

function openContact() { /* modal/contact */ }
function toggleFollow() { /* follow/unfollow */ }
</script>

