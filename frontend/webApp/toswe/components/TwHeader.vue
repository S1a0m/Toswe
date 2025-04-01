<template>
    <div class="banner">
        <div class="header">
            <div class="logo">
                <img src="/public/logo-toswe.png" alt="" class="logo-toswe">
                <h1>Tôswè</h1>
            </div>
            <div class="sign">
                <!--<svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#2D1B14"><path d="M221-120q-27 0-48-16.5T144-179L42-549q-5-19 6.5-35T80-600h190l176-262q5-8 14-13t19-5q10 0 19 5t14 13l176 262h192q20 0 31.5 16t6.5 35L816-179q-8 26-29 42.5T739-120H221Zm-1-80h520l88-320H132l88 320Zm260-80q33 0 56.5-23.5T560-360q0-33-23.5-56.5T480-440q-33 0-56.5 23.5T400-360q0 33 23.5 56.5T480-280ZM367-600h225L479-768 367-600Zm113 240Z"/></svg>-->
                <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="30px" fill="#2D1B14"><path d="M784-120 532-372q-30 24-69 38t-83 14q-109 0-184.5-75.5T120-580q0-109 75.5-184.5T380-840q109 0 184.5 75.5T640-580q0 44-14 83t-38 69l252 252-56 56ZM380-400q75 0 127.5-52.5T560-580q0-75-52.5-127.5T380-760q-75 0-127.5 52.5T200-580q0 75 52.5 127.5T380-400Z"/></svg>
                <TwLoginBtn />
                <TwSignUpBtn />
            </div>
        </div>
        <div class="subheader">
            <div>
                <div>
                    <h1>Nous vendons pour vous.</h1>
                    <p>Accessoires tech, outils menagers, <strong>produits locaux</strong> et bien plus.</p>
                    <button>
                        Telecharger l'application mobile
                        <svg xmlns="http://www.w3.org/2000/svg" height="36px" viewBox="0 -960 960 960" width="36px" fill="#F5E6DA"><path d="M480-320 280-520l56-58 104 104v-326h80v326l104-104 56 58-200 200ZM240-160q-33 0-56.5-23.5T160-240v-120h80v120h480v-120h80v120q0 33-23.5 56.5T720-160H240Z"/></svg>
                    </button>
                </div>
                <img src="/public/images/toswe-montre.png" alt="">
            </div>
        </div>
        <div class="menu">
            <span class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#C0A080"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg>
            </span>
            <span class="active-page">Acceuil</span>
        </div>
        <!--<nav>
            <TwPageLink>Acceuil</TwPageLink>
            <TwPageLink>A propos</TwPageLink>
            <TwPageLink>Nous contacter</TwPageLink>
            <TwPageLink>Telecharger l'app</TwPageLink>
            <TwPageLink>Rechercher un produit</TwPageLink>
            <TwPageLink>Panier</TwPageLink>
        </nav>-->
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
                    family: sans-serif;
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

                font: {
                    size: 30px;
                    weight: bold;
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


    background: rgba(45, 27, 20, 0.3);
    backdrop-filter: blur(10px);
    //flex-direction: column-reverse;

    .icon {
        display: flex;
        align-items: center;
        flex-direction: column;
        background: rgba(45, 27, 20, 0.5);
        backdrop-filter: blur(10px);
        //border-radius: 20px;
        &:hover {
            box-shadow: 0px 1px 4px black;
            cursor: pointer;     
        }
    }

    .active-page {
        color: #F5E6DA;
        
        font: {
            size: 25px;
            weight: bold;
            family: sans-serif;
        }
    }
}

</style>