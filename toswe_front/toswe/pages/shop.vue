<!-- pages/shop.vue -->
<template>
  <div class="min-h-screen">
    <!-- Header -->
    <ShopHeader
      v-if="shop"
      :shop="shop"
      :is-owner="isOwner"
      @contact="openContact"
      @follow="toggleFollow"
    />

    <!-- Skeleton en-tête -->
    <div v-else class="bg-white/90 backdrop-blur border-b">
      <div class="max-w-6xl mx-auto px-4 py-6 animate-pulse">
        <div class="h-10 w-1/3 bg-gray-200 rounded"></div>
        <div class="mt-3 h-4 w-1/2 bg-gray-200 rounded"></div>
      </div>
    </div>

    <!-- Boutique publique -->
    <main class="max-w-6xl mx-auto px-4 py-6" v-if="!isOwner">
      <!-- À propos -->
      <section v-if="shop?.about" class="mb-8">
        <h2 class="font-semibold text-lg mb-2">À propos</h2>
        <p class="text-gray-700 leading-relaxed" :class="{ 'line-clamp-3': !showMore }">
          {{ shop.about }}
        </p>
        <button
          v-if="shop.about.length > 220"
          class="mt-2 text-sm text-[#7D260F] hover:underline"
          @click="showMore = !showMore"
        >
          {{ showMore ? 'Voir moins' : 'Voir plus' }}
        </button>
      </section>

      <!-- Produits -->
      <section class="mb-8">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold text-lg">Produits</h2>
          <div class="text-sm text-gray-500">{{ products?.length || 0 }} résultats</div>
        </div>

        <!-- grid -->
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

        <!-- skeleton -->
        <div
          v-else-if="pending"
          class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 animate-pulse"
        >
          <div v-for="i in 8" :key="i" class="h-56 rounded-xl bg-gray-200"></div>
        </div>

        <!-- empty -->
        <div v-else class="rounded-xl border bg-white p-8 text-center text-gray-600">
          Aucun produit pour le moment.
        </div>
      </section>
    </main>

    <!-- Vue propriétaire -->
    <div v-else class="max-w-6xl mx-auto px-4 py-6">
      <TwMyShop
        :products="products"
        :seller-id="sellerId"
      />
    </div>

    <TwMenuSide />
    <TwCart />
    <TwPopupAd />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'
import { useNavigation } from '@/composables/useNavigation'

const { goToProductDetails } = useNavigation()
const auth = useAuthStore()
const route = useRoute()
const showMore = ref(false)

// En-tête boutique
const { data: shopHeader, pending } = await useAsyncData('shopHeader', () =>
  $fetch(`http://127.0.0.1:8000/api/seller/${route.query.id}/shop_header/`, {
    headers: {
      Authorization: `Bearer ${auth.accessToken}`
    }
  })
)

// Produits
const products = ref([])
async function fetchSellerProducts() {
  try {
    if (!shopHeader.value?.seller_essential?.id) return
    const data = await $fetch(
      `http://127.0.0.1:8000/api/product/${shopHeader.value.seller_essential.id}/seller_products/`
    )
    products.value = data?.results || []
  } catch (err) {
    console.error('Erreur chargement produits du vendeur:', err)
  }
}

const sellerId = shopHeader.value.seller_essential.id
watch(shopHeader, fetchSellerProducts, { immediate: true })


// Shop normalisé
const shop = computed(() =>
  shopHeader.value
    ? {
        id: shopHeader.value.seller_essential?.id,
        is_verified: shopHeader.value.is_verified,
        slogan: shopHeader.value.slogan,
        about: shopHeader.value.about,
        stars_count: shopHeader.value.total_rating?.count,
        stars_avg: shopHeader.value.total_rating?.average,
        seller_user_id: shopHeader.value.seller_essential?.seller_user_id,
        name: shopHeader.value.seller_essential?.shop_name,
        loyal_customers_count: shopHeader.value.seller_essential?.total_subscribers,
        logo_url: shopHeader.value.seller_essential?.logo,
        owner_id: shopHeader.value.seller_essential?.seller_user_id
      }
    : null
)

// Propriétaire ?
const isOwner = computed(() => !!shop.value && auth?.user?.id === shop.value?.owner_id)

function openContact() {
  // TODO
}
function toggleFollow() {
  // TODO
}
</script>
