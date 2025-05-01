<script setup>
import { onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

onMounted(() => {
  cart.loadFromLocalStorage()
})
</script>

<template>
    <div class="template">
      <header>
        <TwHeader />
      </header>
  
      <main>
        <div class="content">
          <div class="blur-inside">
            <slot></slot>
          </div>
        </div>
        <NuxtLink to="/basket#nav-head">
          <div class="basket">
            {{ cart.totalInBasket }}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960">
              <path d="M221-120q-27 0-48-16.5T144-179L42-549q-5-19 6.5-35T80-600h190l176-262q5-8 14-13t19-5q10 0 19 5t14 13l176 262h192q20 0 31.5 16t6.5 35L816-179q-8 26-29 42.5T739-120H221Zm-1-80h520l88-320H132l88 320Zm260-80q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM367-600h225L479-768 367-600Zm113 240Z"/>
            </svg>
          </div>
        </NuxtLink>
      </main>
  
      <footer>
        <TwFooter />
      </footer>
    </div>
    <TwCookie />
    <TwAlert />
</template>
  
<style lang="scss" scoped>
.blur-inside {
  backdrop-filter: blur(10px);
  min-height: 100vh;
}

.content {
  background-image: url("/public/images/toswe-africa-art.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  min-height: 100vh;
}

.template {
    // height: 100vh;
    background: radial-gradient(circle, #7D260F 8%, #2D1B14 100%);
}

.basket {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #0d0d0d;
  color: #C0A080;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  svg {
    width: 28px;
    height: 28px;
    fill: #C0A080;
    transition: transform 0.3s ease;
  }

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(192, 160, 128, 0.3);

    svg {
      transform: scale(1.1);
    }
  }

  @media (max-width: 600px) {
    bottom: 1rem;
    right: 1rem;
    padding: 0.5rem 0.75rem;
    font-size: 1rem;

    svg {
      width: 24px;
      height: 24px;
    }
  }
}

</style>
  