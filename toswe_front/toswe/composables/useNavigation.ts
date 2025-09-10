import { useInteractionsStore } from '@/stores/interactions'

export function useNavigation() {

    function goToProductDetails(productId: number) {
        const interactions = useInteractionsStore()
        interactions.addInteraction('view', productId, "product details viewed")
        return navigateTo({ path: "/product", query: { id: productId } })
    }

    function goToShopDetails(shopId: number) {
        const interactions = useInteractionsStore()
        interactions.addInteraction('view', shopId, "shop details viewed")
        return navigateTo({ path: "/shop", query: { id: shopId } })
    }

    return {
        goToProductDetails,
        goToShopDetails
    }
}