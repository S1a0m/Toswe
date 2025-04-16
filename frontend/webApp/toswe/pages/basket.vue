<script setup>
import { useCartStore } from "@/stores/cart"

const cart = useCartStore()
</script>

<template>
  <div class="about-content">
    <section>
      <h2>· Commande ·</h2>
      <div class="order-table">
        <div class="title-row">
          <span>Nom du produit</span>
          <span>Image</span>
          <span>Prix unitaire</span>
          <span>Quantité</span>
          <span>Total</span>
          <span>Supprimer</span>
        </div>

        <div v-if="cart.items.length > 0">
        <TwArticleItem
          v-for="item in cart.items"
          :key="item.id"
          :id="item.id"
          :name="item.name"
          :price="item.price"
          :total="item.price * item.quantity"
          :img="item.img"
          :number="item.quantity"
        />
        <h3 class="total-row last-row">Total : {{ cart.totalAmount }} fcfa</h3><br>
        <button type="submit">
          Soummettre
          <svg xmlns="http://www.w3.org/2000/svg" height="25px" viewBox="0 -960 960 960" width="25px" fill="#2D1B14"><path d="M560-440q-50 0-85-35t-35-85q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35ZM280-320q-33 0-56.5-23.5T200-400v-320q0-33 23.5-56.5T280-800h560q33 0 56.5 23.5T920-720v320q0 33-23.5 56.5T840-320H280Zm80-80h400q0-33 23.5-56.5T840-480v-160q-33 0-56.5-23.5T760-720H360q0 33-23.5 56.5T280-640v160q33 0 56.5 23.5T360-400Zm440 240H120q-33 0-56.5-23.5T40-240v-440h80v440h680v80ZM280-400v-320 320Z"/></svg>
        </button>
      </div>
      <p class="last-row" v-else>Votre panier est vide.</p>

      </div>
    </section><br><br><br>
  </div>
</template>
  

<style lang="scss" scoped>
.about-content {
  padding: 40px 80px 80px 80px;
}

section {
  h2 {
    color: #EFE8E8;
    font-family: "Playfair Display";
  }
}

.order-table {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  font-family: "Lora";

  .title-row, .order-row {
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

  .title-row {
    background: rgba(239, 232, 232, 0.5);
    font-weight: 600;
    font-family: "Inter";
  }
}

.last-row {
    background: rgba(239, 232, 232, 0.5);
    font-weight: 600;
    font-family: "Inter";
    border-radius: 15px;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #7D260F;
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2D1B14;
  // background: #F5E6DA;
  background: rgba(245, 230, 218, 0.2);
  border-color: #2D1B14;
  // border-radius: 30px;
  height: 60px;
  width: 200px;
  cursor: pointer;
  transition: all 0.5s 0s ease;
  border-radius: 12px;
  font: {
    size: 18px;
    weight: 500;
    family: "Inter"
  }

  &:hover {
    background: rgba(245, 230, 218, 1);
  }
}

input {
  background: none;
  font-size: 18px;
  font-family: "Lora";
  width: 80px;
  border-top: none;
  border-left: none;
  border-right: none;
  color: #EFE8E8;
}

.del-product {
  cursor: pointer;
}
</style>