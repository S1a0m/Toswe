import { useInteractionsStore } from '@/stores/interactions'

export function useNavigation() {

    function goToProductDetails(productId: number) {
        const interactions = useInteractionsStore()
        interactions.addInteraction('view', productId, "product details viewed")
        return navigateTo({ path: "/product", query: { id: productId } })
    }

    return {
        goToProductDetails
    }
}