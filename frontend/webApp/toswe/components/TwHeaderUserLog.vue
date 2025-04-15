<script setup>

</script>

<template>
    <div class="banner">
        <div class="header">
            <div class="logo">
                <img src="/public/logo-toswe.png" alt="" class="logo-toswe">
                <h1>Tôswè.africa - Admin</h1>
            </div>
            <div class="sign">
                <NuxtLink to="/"><span class="sign">Consulter sur le site</span></NuxtLink>
            </div>
        </div>
    </div>
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
            width: 70px;
            height: 70px;
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
        color: rgb(45, 27, 20);
        font-family: "Inter";
        text-decoration: underline;

        &:hover {
            color: rgba(45, 27, 20, 0.8);
        }
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
        // transform: scale(1.15);
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