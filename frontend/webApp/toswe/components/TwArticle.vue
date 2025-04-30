<script setup>
import { useCartStore } from "@/stores/cart"

const props = defineProps([
  "id",
  "img",
  "name",
  "price",
])

const router = useRouter()
const isAdded = ref(false)
const isAnimating = ref(false)

const cart = useCartStore()

const product = {
    id: props.id,
    img: props.img,
    name: props.name,
    price: props.price
}

function handleAddClick() {
  if (isAdded.value) {
    router.push('/basket#nav-head')
    return
  }

  cart.addToCart(product)
  isAdded.value = true
  isAnimating.value = true

  setTimeout(() => {
    isAnimating.value = false
  }, 300)
}
</script>


<template>
    <article>
        <NuxtLink :to="{name: 'product', hash: '#nav-head',  query: {id: props.id}}">
            <div class="image-wrapper">
                <img :src="props.img" alt="" />
                <div class="see-more">Voir plus...</div>
            </div>
        </NuxtLink>
        <div>
            <h3>{{ props.name }} ···</h3> 
            <p>{{ props.price }} fcfa</p>
        </div>
        <div>
            <button
                type="button"
                :class="{ animate: isAnimating }"
                @click="handleAddClick"
            >
                {{ isAdded ? "Panier" : "Ajouter" }}
                <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#C0A080"><path d="M444-576v-132H312v-72h132v-132h72v132h132v72H516v132h-72ZM263.79-96Q234-96 213-117.21t-21-51Q192-198 213.21-219t51-21Q294-240 315-218.79t21 51Q336-138 314.79-117t-51 21Zm432 0Q666-96 645-117.21t-21-51Q624-198 645.21-219t51-21Q726-240 747-218.79t21 51Q768-138 746.79-117t-51 21ZM48-792v-72h133l155 360h301l113-264h78L703-476q-9 20-26.5 32T637-432H317l-42 72h493v72H276q-42 0-63-36.5t0-71.5l52-90-131-306H48Z"/></svg>
            </button>
        </div>
    </article>
</template>

<style lang="scss" scoped>
article {
    background: rgba(245, 230, 218, 0.7);
    width: 325px;
    height: 420px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    backdrop-filter: blur(4px);
    transition: all 0.45s 0s ease;

    &:hover {
        transform: translateY(-10px);
        box-shadow: 0px 1px 4px black;
    }

    img {
        width: 280px;
        height: 280px;
        cursor: pointer;
    }

    div {
        display: flex;
        align-items: center;
        // justify-content: space-between;
        gap: 20px;
        color: #7D260F;
        margin: 15px 0px 0px 0px ;
        h3 {
            color: rgb(45, 27, 20);
            font: {
                size: 25px;
                family: "Lora";
            }   
        }

        p {
            font: {
                size: 22px;
                family: "Lora";
                weight: 600;
            } 
        }
    }

    div {
        button {
            background: #7D260F;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #C0A080;
            width: 100px;
            height: 40px;
            border: none;
            border-radius: 15px;
            border-style: solid;
            border-width: 1px;
            cursor: pointer;

            font: {
                size: 16px;
                weight: bold;
                family: "Inter"
            }

            &:hover {
                box-shadow: 0px 1px 4px black;
                border: none;
            }
        }
    }
}

.image-wrapper {
  position: relative;
  width: 280px;
  height: 280px;

  img {
    width: 100%;
    height: 100%;
    display: block;
    border-radius: 10px;
  }

  .see-more {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    background: rgba(0, 0, 0, 0.5);
    padding: 8px 16px;
    border-radius: 8px;
    opacity: 0;
    transition: opacity 0.3s ease;
    font-family: "Inter", sans-serif;
    font-size: 14px;
    pointer-events: none;
  }

  &:hover .see-more {
    opacity: 1;
  }
}

button.animate {
  animation: bounce 0.3s ease;
}

@keyframes bounce {
  0% { transform: scale(1); }
  30% { transform: scale(1.15); }
  60% { transform: scale(0.95); }
  100% { transform: scale(1); }
}


.more {
    font: {
        size: 12px;
    }
}

a {
    text-decoration: none;
}

</style>

