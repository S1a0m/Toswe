<script setup>
import { ref } from "vue";
import { useRoute } from 'vue-router';


const route = useRoute();
const activePage = ref(null);

// Fonction pour mettre à jour activePage en fonction de la route
const updateActivePage = () => {
  switch (route.path) {
    case "/":
      activePage.value = 'Accueil';
      break;
    case "/about":
      activePage.value = 'À propos';
      break;
    case "/contact":
      activePage.value = 'Nous contacter';
      break;
    case "/basket":
      activePage.value = 'Panier';
      break;
    case "/rules":
      activePage.value = 'Politiques d utilisation du site';
      break;
    case "/product":
      activePage.value = 'Produit';
      break;
    default:
      activePage.value = 'Page inconnue';
  }
};

watch(route, updateActivePage, { immediate: true });

const searchPopup = ref(null);

const openSearchPopup = () => {
  if (searchPopup.value) {
    searchPopup.value.showPopup = true;
  }
};

const showMenu = ref(false);

const toggleMenu = () => {
    showMenu.value = !showMenu.value;
}

const showSearchPopup = ref(false);

const toggleSearchPopup = () => {
    showSearchPopup.value = !showSearchPopup.value;
}

const showPopup = ref(false);

// S'affiche automatiquement au chargement de la page
onMounted(() => {
  showPopup.value = true;
});

const redirectToStore = () => {
  if (/Android/i.test(navigator.userAgent)) {
    window.open("https://play.google.com/store/apps/details?id=ton.app.id", "_blank");
  } else if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) {
    window.open("https://apps.apple.com/app/idtonappid", "_blank");
  } else {
    showPopup.value = true;
  }
};

</script>

<template>
    <div class="banner">
        <div class="header">
            <NuxtLink to="/">
                <div class="logo">
                    <img src="/public/Tw7_2.png" alt="" class="logo-toswe">
                    <h1><!--Tôswè-->.africa</h1>
                </div>
            </NuxtLink>
            <div class="sign">
                <!--<svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#2D1B14"><path d="M221-120q-27 0-48-16.5T144-179L42-549q-5-19 6.5-35T80-600h190l176-262q5-8 14-13t19-5q10 0 19 5t14 13l176 262h192q20 0 31.5 16t6.5 35L816-179q-8 26-29 42.5T739-120H221Zm-1-80h520l88-320H132l88 320Zm260-80q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM367-600h225L479-768 367-600Zm113 240Z"/></svg>-->
                <div @click="toggleSearchPopup" class="search-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#2D1B14"><path d="M784-120 532-372q-30 24-69 38t-83 14q-109 0-184.5-75.5T120-580q0-109 75.5-184.5T380-840q109 0 184.5 75.5T640-580q0 44-14 83t-38 69l252 252-56 56ZM380-400q75 0 127.5-52.5T560-580q0-75-52.5-127.5T380-760q-75 0-127.5 52.5T200-580q0 75 52.5 127.5T380-400Z"/></svg>
                </div>
                <TwSearch v-if="showSearchPopup" @close-searchpopup="toggleSearchPopup"/>
                <TwLoginBtn @click="redirectToStore"/>
                <TwSignUpBtn @click="redirectToStore"/>
            </div>
        </div>
        <div class="subheader">
            <div>
                <div>
                    <h1>Nous vendons pour vous.</h1>
                    <p>Accessoires tech, outils menagers, <strong>produits locaux</strong> et bien plus.</p>
                    <button @click="showPopup = true" class="open-popup-btn">
                        Telecharger l'application mobile
                        <svg xmlns="http://www.w3.org/2000/svg" height="36px" viewBox="0 -960 960 960" width="36px" fill="#F5E6DA"><path d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/></svg>
                    </button>
                </div>
                <img src="/public/images/toswe-montre.png" alt="">
            </div>
        </div>
        <div class="main-menu">
            <div class="menu" id="nav-head">
                <span @click="toggleMenu" class="icon">
                    <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#C0A080"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg>
                </span>
                <span class="active-page">{{ activePage }}</span>
            </div>
            <transition name="slide-up-menu">
            <nav v-if="showMenu">
                <TwPageLink link="/#nav-head">Acceuil</TwPageLink>
                <TwPageLink link="/about#nav-head">A propos</TwPageLink>
                <TwPageLink link="/contact#nav-head">Nous contacter</TwPageLink>
                <!--<TwPageLink>Telecharger l'app</TwPageLink>-->
                <!--<TwPageLink>Rechercher un produit</TwPageLink>-->
                <TwPageLink link="/basket#nav-head">Panier</TwPageLink>
            </nav>
            </transition>
        </div>
    </div>
    <TwDownloadApp :showPopup="showPopup" @close="showPopup = false" />
</template>

<style lang="scss" scoped>
.header {
    background-color: rgba(245, 230, 218, 0.5);
    // backdrop-filter: blur;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;

    .logo {
        display: flex;
        align-items: center;

        .logo-toswe {
            width: 150px;
            height: 50px;
        }

        h1 {
            color: #7D260F;
            font-family: "Playfair Display";
            font-weight: 900;
        }
    }

    .sign {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-right: 8px;
    }
}

.subheader {
    // height: 533px;
    // background: radial-gradient(circle, #7D260F 8%, #2D1B14 100%);
    display: flex;
    justify-content: space-around;
    //flex-direction: column;

    div {
        display: flex;
        div {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 50px;
            gap: 30px;

            h1 {
                color: #C0A080;
                font: {
                    size: 60px;
                    weight: 100;
                    family: "Inter";
                }
            }

            p {
                color: #F5E6DA;
                background: rgba(45, 27, 20, 0.3);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                width: 941px;
                padding: 20px;
                font: {
                    size: 60px;
                    weight: 300;
                    family: "Lora";
                }  
            }

            button {
                // color: #2D1B14;
                color: #F5E6DA;
                display: flex;
                justify-content: center;
                align-items: center;
                border-radius: 20px;
                border-width: 1px;
                background-color: rgba(192, 160, 128, 0);
                // border: none;
                width: 549px;
                height: 80px;
                cursor: pointer;
                transition: all 0.5s 0s ease;

                &:hover {
                    color: #7D260F;
                    background: #F5E6DA;
                }

                &:hover svg {
                    fill: #7D260F;
                }

                font: {
                    size: 30px;
                    weight: 600;
                    family: "Inter";
                }
            }
        }
    }

    img {
        height: 610px;
    }
}

nav {
    // background: rgba(245, 230, 218, 0.9);
    // background: rgba(125, 38, 15, 100);
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    box-shadow: 0px 1px 1px black
}

.menu {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 10px;
    border-style: solid;
    border-left: none;
    border-right: none;
    border-width: 1px;
    border-color: rgba(45, 27, 20, 0.5);
    position: sticky;


    background: rgba(45, 27, 20, 0.3);
    backdrop-filter: blur(10px);
    //flex-direction: column-reverse;

    .icon {
        display: flex;
        align-items: center;
        flex-direction: column;
        // background: rgba(45, 27, 20, 1);
        backdrop-filter: blur(10px);
        //border-radius: 20px;
        &:hover {
            box-shadow: 0px 1px 4px black;
            cursor: pointer;     
        }
    }

    .active-page {
        color: #C0A080;
        
        font: {
            size: 22px;
            weight: bold;
            family: "Inter";
        }
    }
}

.search-btn {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s 0s ease;
    height: 40px;
    width: 40px;

    &:hover {
        box-shadow: 0px 1px 4px black;
    }
}

a {
  text-decoration: none;
}

  /* Animation d'apparition et disparition */
  .slide-up-menu-enter-active,
  .slide-up-menu-leave-active {
    transition: transform 0.5s ease-out, opacity 0.5s ease-in;
  }
  
  .slide-up-menu-enter-from,
  .slide-up-menu-leave-to {
    transform: translateX(-80%);
    opacity: 0;
  }
</style>