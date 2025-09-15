import { useInteractionsStore } from '@/stores/interactions'
import { useAuthStore } from '@/stores/auth'

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

    function goToMyShop() {
        const auth = useAuthStore()
        if (auth.user && auth.user.is_seller) {
            return navigateTo({ path: "/shop", query: { id: auth.user.id } })
        }
    }

    function goToOrderDetails(orderId: number) {
        return navigateTo({ path: "/order", query: { id: orderId } })
    }

    return {
        goToProductDetails,
        goToShopDetails,
        goToMyShop,
        goToOrderDetails
    }
}