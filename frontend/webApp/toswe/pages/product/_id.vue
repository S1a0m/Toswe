<script setup>
// Liste des slides du carrousel produit
const slideList = [
  { id: 1, src: '/images/montre.jpg' },
  { id: 2, src: '/images/chargeur.jpg' },
  { id: 3, src: '/images/img3.jpg' },
]
</script>

<template>
  <div class="about-content">
    <!-- Section Produit -->
    <section>
      <h2>· Produit ·</h2>
      <div class="product-details">
        <!-- Image du produit -->
        <div class="product-image">
          <TwCarouselProductOverview :slides="slideList" />
        </div>

        <!-- Détails et actions -->
        <div class="product-actions">
          <div class="price">
            <h3 class="product-name">Chargeur</h3>
            <span class="product-price">4 500 fcfa</span><br>
            <span class="product-category"><strong>Produit électronique</strong></span><br>
            <span class="in-stock">En stock</span>
          </div>

          <div class="order-actions">
            <button>Ajouter au panier</button><br><br><br>
            <div class="go-order">
              <NustLink>
                <span class="gone-order">
                  Voir d'autres versions
                  <svg xmlns="http://www.w3.org/2000/svg" height="20" viewBox="0 -960 960 960" width="20" fill="#C0A080">
                    <path d="M440-800v487L216-537l-56 57 320 320 320-320-56-57-224 224v-487h-80Z"/>
                  </svg>
                </span>
              </NustLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <br><br><br>

    <!-- Section Description -->
    <section>
      <h2>· Description ·</h2>
      <p>
        Son haute définition : Profitez de basses profondes et de sons cristallins grâce à la technologie X-BASS Boost. 
        Bluetooth 5.0 : Connexion ultra-stable jusqu’à 15 mètres de distance. 
        Autonomie longue durée : Jusqu’à 12 heures de musique non-stop avec une seule charge.<br><br>

        Caractéristiques :<br>
        · Résistante à l’eau (IPX7) : Parfaite pour la plage, la piscine ou la douche.<br>
        · Mode Party Connect : Associez plusieurs enceintes pour une ambiance encore plus intense.<br>
        · Port USB & Micro SD : Lisez vos musiques directement sans Bluetooth.
      </p>
    </section>

    <br><br><br>

    <!-- Section Autres Versions -->
    <section class="testimony">
      <h2>· Autres versions du produit ·</h2>
      <div class="mix">
        <div class="bkgcolors">
          <div class="testimoner">
            <div class="other-versions">
              <img src="/public/images/montre.jpg" alt="" class="version" />
              <img src="/public/images/chargeur.jpg" alt="" class="version" />
              <img src="/public/images/trepied.png" alt="" class="version" />
              <img src="/public/images/table-royal.webp" alt="" class="version" />
              <img src="/public/images/toswe-montre.png" alt="" class="version" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <br><br><br>
  </div>
</template>

<style lang="scss" scoped>
.about-content {
  padding: 40px 80px 80px;
}

section {
  h2 {
    color: #EFE8E8;
    font-family: "Playfair Display";
  }

  p {
    margin-top: 20px;
    padding: 15px;
    background: rgba(239, 232, 232, 0.5);
    color: #2D1B14;
    backdrop-filter: blur(4px);
    border-radius: 20px;
    width: fit-content;

    font-size: 18px;
    font-family: "Lora";
  }
}

.testimony {
  .mix {
    margin-top: 20px;
    background: rgba(45, 27, 20, 1);

    .bkgcolors {
      background: rgba(239, 232, 232, 0.1);
      height: 100%;
    }
  }
}

.testimoner {
  display: flex;
  align-items: center;
  gap: 50px;
  padding: 100px;
}

.other-versions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 80px;
  overflow-x: auto;
  white-space: nowrap;
  scroll-behavior: smooth;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.version {
  width: 323px;
  height: 340px;
  object-fit: cover;
}

.product-details {
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}

.product-image {
  width: 544px;
  height: 544px;
  border-radius: 10px;
  background: rgba(245, 230, 218, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.active-product {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  width: 400px;
}

.product-name {
  color: #F5E6DA;
  font-size: 48px;
  font-family: "Lora";
}

.product-price {
  color: #F5E6DA;
  font-size: 70px;
  font-family: "Lora";
}

.product-category, .in-stock {
  font-size: 36px;
  font-family: "Lora";
}

.product-category {
  color: #F5E6DA;
}

.in-stock {
  color: green;
}

.product-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 30px;
}

button {
  width: 500px;
  height: 60px;
  cursor: pointer;
  color: #2D1B14;
  border: 1px solid #2D1B14;
  background: rgba(192, 160, 128, 0.1);
  font-size: 30px;
  transition: background 0.5s ease;

  &:hover {
    background: rgba(192, 160, 128, 1);
  }
}

.gone-order {
  color: #C0A080;
  font-family: "Inter";
  font-weight: bold;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: font-weight 0.5s ease;

  &:hover {
    font-weight: 800;
  }
}
</style>
