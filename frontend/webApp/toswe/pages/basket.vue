<template>
  <div class="about-content">
    <section>
      <h2>· Conditions Générales de Vente (CGV) ·</h2>
      <div class="order-table">
        <div class="title">
          <span>Nom du produit</span>
          <span>Image</span>
          <span>Prix unitaire(en fcfa)</span>
          <span>Nombre dans le panier</span>
          <span>Total(en fcfa)</span>
        </div><br><br>
        <div class="products">
          <div class="order">
            <div class="product">
              <h4>Ouffer</h4>
              <img src="/public/images/table-royal.webp" alt="">
              <span>7 500</span>
              <input type="number" name="" id="" placeholder="00">
              <span>15 000</span>
            </div>
              <div class="del-product">
                <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#C0A080"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>
              </div>
          </div><br><br>
          <div class="order">
            <div class="product">
              <h4>Ouffer</h4>
              <img src="/public/images/table-royal.webp" alt="">
              <span>7 500</span>
              <input type="number" name="" id="" placeholder="00">
              <span>15 000</span>
            </div>
              <div class="del-product">
                <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#C0A080"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>
              </div>
          </div><br><br>
          <div class="order">
            <div class="product">
              <h4>Ouffer</h4>
              <img src="/public/images/table-royal.webp" alt="">
              <span>7 500</span>
              <input type="number" name="" id="" placeholder="00">
              <span>15 000</span>
            </div>
              <div class="del-product">
                <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#C0A080"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>
              </div>
          </div>
        </div>
      </div>
    </section><br><br><br>
    <button type="submit">
      Soummettre
      <svg xmlns="http://www.w3.org/2000/svg" height="25px" viewBox="0 -960 960 960" width="25px" fill="#2D1B14"><path d="M560-440q-50 0-85-35t-35-85q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35ZM280-320q-33 0-56.5-23.5T200-400v-320q0-33 23.5-56.5T280-800h560q33 0 56.5 23.5T920-720v320q0 33-23.5 56.5T840-320H280Zm80-80h400q0-33 23.5-56.5T840-480v-160q-33 0-56.5-23.5T760-720H360q0 33-23.5 56.5T280-640v160q33 0 56.5 23.5T360-400Zm440 240H120q-33 0-56.5-23.5T40-240v-440h80v440h680v80ZM280-400v-320 320Z"/></svg>
    </button>
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
  .title {
    background: rgba(239, 232, 232, 0.7);
    backdrop-filter: blur(4px);
    height: 98px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    font-family: "Inter";

    span {
      font: {
        size: 18px;
        weight: 600;
      }
    }
  }

  .products {

    .order {
      gap: 10px;
      font-family: "Lora";

      .product {
        background: rgba(239, 232, 232, 0.2);
        backdrop-filter: blur(4px);
        // height: 98px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: space-around;
        padding: 1em;

        img {
          height: 200px;
          width: 200px;
        }

        span, h4 {
          color: #EFE8E8;
          font: {
            size: 18px;
          }
        }
      }
    }
  }
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