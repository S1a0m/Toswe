<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

definePageMeta({
  prerender: true
})

const slides = ref([
  {
    id: 1,
    image: "/images/img1.jpg",
    testimonial: "Cette application a radicalement transformé ma manière de collaborer avec mon équipe. Elle est rapide, sécurisée et incroyablement intuitive.",
    name: "Amina Traoré"
  },
  {
    id: 2,
    image: "/images/img2.jpg",
    testimonial: "Un vrai coup de cœur ! L’interface est fluide, et le support client est à l’écoute et très réactif.",
    name: "Jean-Baptiste Kouassi"
  },
  {
    id: 3,
    image: "/images/img3.jpg",
    testimonial: "Une solution complète qui répond parfaitement à mes exigences en matière de sécurité et de confidentialité.",
    name: "Fatou Diop"
  },
  {
    id: 4,
    image: "/images/img4.jpg",
    testimonial: "Simple, efficace et ultra fiable. Aujourd’hui, je ne peux plus m’en passer.",
    name: "Mohamed Cissé"
  }
])

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
        Bienvenue chez <strong>Tôswè</strong>, votre boutique en ligne de confiance ! Nous vous livrons des produits de qualité directement chez vous — sans intermédiaires ni complications. <br><br>

        Notre mission ? Rendre votre expérience d’achat simple, rapide et 100 % sécurisée. Nous sélectionnons avec soin des articles tendances, innovants et à des prix imbattables. Grâce au dropshipping, nous collaborons avec des fournisseurs fiables pour vous offrir un large choix : mode, high-tech, maison, accessoires… il y en a pour tous les goûts ! <br><br>

        <strong>Pourquoi choisir Tôswè ?</strong><br>
        ▸ <strong>Qualité garantie :</strong> chaque produit est choisi avec rigueur pour vous satisfaire durablement.<br>
        ▸ <strong>Prix abordables :</strong> des offres exceptionnelles sans compromis sur la qualité.<br>
        ▸ <strong>Livraison rapide et fiable :</strong> recevez vos colis à domicile sans stress.<br>
        ▸ <strong>Support réactif :</strong> contactez-nous facilement via WhatsApp ou par e-mail, on vous répond vite !<br><br>

        Basés à Abomey-Calavi, nous sommes fiers de servir toute la région… et bien plus encore !
      </p>
    </section><br><br><br>

    <section>
      <h2>· Objectif ·</h2>
      <p>
        Révolutionner le commerce au Bénin, en Afrique… et dans le monde entier.
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
      <div class="founders">
        <div class="founder-card" v-intersect>
          <img src="/images/jack.jpg" alt="David I." />
          <div class="info">
            <span><strong>David I.</strong></span>
            <p>
              <strong>Co-fondateur & COO — Responsable Commercial et Relation Client</strong><br>
              C’est avec lui que vous communiquez très souvent lorsque vous nous contactez.<br><br>
              Facebook: David Idohou
            </p>
          </div>
        </div>

        <div class="founder-card">
          <img src="/images/gojo.jpg" alt="Precieux A." />
          <div class="info">
            <span><strong>Precieux A.</strong></span>
            <p>
              <strong>Co-fondateur & CTO — Responsable Design et Développement</strong><br>
              Il s’occupe le plus souvent de la livraison et est développeur chez Tôswè.<br><br>
              LinkedIn: Précieux Samson Amoussou<br>
              Facebook: Précieux Amoussou
            </p>
          </div>
        </div>
      </div>
    </section><br><br><br>
  </div>
</template>

  

<style lang="scss" scoped>
.about-content {
  padding: 40px 80px 80px 80px;
  backdrop-filter: blur(10px);
  min-height: 100vh;
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
    border-radius: 20px;

    .bkgcolors {
      position: relative;
      overflow: hidden;
      background: rgba(239, 232, 232, 0.1);
      border: none;
      // width: 100%;
      // height: 100%;
      min-height: 540px; 
      border-radius: 20px;
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

.founders {
  margin-top: 20px;
  display: flex;
  gap: 60px;
  flex-wrap: wrap;
  justify-content: center;

  .founder-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(239, 232, 232, 0.15);
    border-radius: 20px;
    padding: 30px;
    width: 320px;
    text-align: center;
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      background: rgba(239, 232, 232, 0.2);
    }

    img {
      width: 200px;
      height: 200px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 20px;
      border: 2px solid #EFE8E8;
    }

    .info {
      span {
        color: #EFE8E8;
        font-family: "Lora";
        font-size: 20px;
      }

      p {
        color: #2D1B14;
        font-family: "Lora";
        margin-top: 10px;
        font-size: 16px;
        background: transparent;
        padding: 0;
      }
    }
  }
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