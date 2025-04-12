<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const slides = ref([
  {
    "id": 1,
    "image": "/images/img1.jpg",
    "testimonial": "Cette application a totalement changé la façon dont je communique avec mon équipe. Elle est rapide, sécurisée et intuitive.",
    "name": "Amina Traoré"
  },
  {
    "id": 2,
    "image": "/images/img2.jpg",
    "testimonial": "Je recommande vivement ! L'interface est fluide et le service client est à l'écoute.",
    "name": "Jean-Baptiste Kouassi"
  },
  {
    "id": 3,
    "image": "/images/img3.jpg",
    "testimonial": "Une solution complète pour mes besoins en sécurité et en partage confidentiel.",
    "name": "Fatou Diop"
  },
  {
    "id": 4,
    "image": "/images/img4.jpg",
    "testimonial": "Simple, efficace, et surtout très fiable. Je ne peux plus m’en passer !",
    "name": "Mohamed Cissé"
  }
]
)

// alert(slides[currentIndex].src);

const currentIndex = ref(0)
let interval

onMounted(() => {
  interval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % slides.value.length
  }, 3000)
})

onUnmounted(() => clearInterval(interval))
</script>

<template>
  <div class="about-content">
    <section>
      <h2>· Description ·</h2>
      <p>
        Bienvenue chez Tôswè, votre boutique en ligne de référence pour des produits de qualité livrés directement chez vous, sans intermédiaires ! <br><br>

Notre mission est de vous offrir une expérience d’achat simple, rapide et sécurisée en sélectionnant avec soin des articles tendances et innovants à des prix compétitifs. Grâce à notre modèle de dropshipping, nous travaillons avec des fournisseurs de confiance pour vous proposer un large choix de produits, allant de la mode aux gadgets high-tech, en passant par les accessoires de maison et bien plus encore. <br><br>

Pourquoi nous choisir ? <br> > Produits de qualité : Nous choisissons nos articles avec rigueur pour garantir satisfaction et durabilité. > Prix abordables : Profitez d'offres attractives sans compromis sur la qualité. > Livraison rapide et fiable : Recevez vos commandes à domicile sans stress. > Service client réactif : Notre équipe est disponible pour répondre à toutes vos questions via WhatsApp et e-mail. <br><br>

Nous sommes basés à Abomey-Calavi
      </p>
    </section><br><br><br>
    <section>
      <h2>· Objectif ·</h2>
      <p>
        Revolutionner le système commercial au Bénin, en Afrique et dans le monde
      </p>
    </section><br><br><br>
    <section class="testimony">
      <h2>· Témoignages ·</h2>
      <div class="mix">
        <div class="bkgcolors">
          <transition name="slide-horizontal" mode="out-in">
            <div class="testimoner" :key="currentIndex">
              <img :src="slides[currentIndex].image" alt="">
              <div>
                <p>
                  "{{ slides[currentIndex].testimonial }}"
                </p>
                <span>— {{ slides[currentIndex].name }}</span>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </section><br><br><br>
    <section>
      <h2>· Fondateurs ·</h2>
      <div class="fonders">
        <div class="dav">
          <img src="/public/images/jack.jpg" alt="">
          <span><strong>David I.</strong></span>
          <p>
            Cofondateur de Tôswè,
C’est avec lui que vous communiquez très souvent
lorsque nous contactez.

                                              Facebook: David Idohou
          </p>
        </div>
        <hr>
        <div class="sam">
          <img src="/public/images/gojo.jpg" alt=""><br><br>
          <span><strong>Precieux A.</strong></span>
          <p>
            Cofondateur de Tôswè,
Il s’occupe le plus souvent de la livraison et est
développeur chez Tôswè.

Linkdin: Précieux Samson Amoussou
Facebook: Précieux Amoussou
          </p>
        </div>
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

  & p {
    margin-top: 20px;
    padding: 15px;
    background: rgba(239, 232, 232, 0.5);
    color: #2D1B14;
    backdrop-filter: blur(4px);
    border-radius: 20px;
    width: fit-content;

    font: {
      size: 18px;
      family: "Lora";
    };
  }
}

.testimony {
  .mix {
    margin-top: 20px;
    // height: 519px;
    // width: 100%;
    background: rgba(45, 27, 20, 1);

    .bkgcolors {
      position: relative;
      overflow: hidden;
      background: rgba(239, 232, 232, 0.1);
      border: none;
      // width: 100%;
      // height: 100%;
      min-height: 540px; 
    }
  }
}

.testimoner {
  display: flex;
  align-items: center;
  // justify-content: space-around;
  gap: 50px;
  padding: 100px;
  inset: 0;
  object-fit: cover;

  div {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;

    span {
      color: #EFE8E8;
      font: {
        size: 20px;
        family: "Lora";
      }
    }
  }
}

img {
  width: 323px;
  height: 340px;
}

.fonders {
  margin-top: 20px;
  display: flex;
  align-items: center;
  // flex-wrap: wrap;
  // justify-content: space-between;
  gap: 80px;
}

.dav {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-direction: column;

  span {
    color: #EFE8E8;
    font: {
      size: 20px;
      family: "Lora";
    }
  }
}

.sam {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-direction: column;

  span {
    color: #EFE8E8;
    font: {
      size: 20px;
      family: "Lora";
    }
  }
}

hr {
  height: 400px;
  color: rgba(239, 232, 232, 0.2);
}

:deep(.slide-horizontal-enter-active),
:deep(.slide-horizontal-leave-active) {
  transition: transform 0.5s ease;
  position: absolute;
  width: 100%;
}
:deep(.slide-horizontal-enter-from) {
  transform: translateX(100%);
}
:deep(.slide-horizontal-leave-to) {
  transform: translateX(-100%);
}

</style>