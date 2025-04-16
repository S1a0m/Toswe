<script setup>
import { ref, watch, computed } from "vue"
import { useCartStore } from "@/stores/cart"

const props = defineProps([
    "id",
    "name",
    "price",
    "total",
    "img",
    "number"
])

const cart = useCartStore()

const quantity = ref(props.number)

watch(quantity, (newVal) => {
  cart.updateQuantity(props.id, Number(newVal))
})

const itemTotal = computed(() => props.price * quantity.value)
</script>

<template>

    <div class="order-row">
      <span class="product-name">{{ props.name }}</span>
      <img :src="props.img" alt="" />
      <span>{{ props.price }}</span>
      <input type="number" min="1" v-model="quantity" />
      <span>{{ itemTotal }}</span>
      <div @click="cart.removeFromCart(props.id)" class="del-product">
        <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#C0A080"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>
      </div>
    </div>
<br>
</template>

<style scoped lang="scss">
.order-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 0.5fr;
    align-items: center;
    padding: 10px 20px;
    border-radius: 15px;
    backdrop-filter: blur(4px);
    background: rgba(239, 232, 232, 0.2);
    color: #EFE8E8;
    gap: 10px;

    span, input {
    font-size: 16px;
    text-align: center;
    }

    img {
    height: 100px;
    width: 100px;
    object-fit: cover;
    border-radius: 10px;
    justify-self: center;
    }

    input {
    background: none;
    border: none;
    border-bottom: 1px solid #EFE8E8;
    width: 60px;
    text-align: center;
    color: #EFE8E8;
    }

    .del-product {
    justify-self: center;
    cursor: pointer;
    }
}
</style>