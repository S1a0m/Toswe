<template>
    <article>
        <img src="/public/images/table-royal.webp" alt="">
        <div>
            <h3>Table</h3>
            <p>25 300 fcfa</p>
        </div>
        <div>
            <button type="button">
                Ajouter
                <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#C0A080"><path d="M440-600v-120H320v-80h120v-120h80v120h120v80H520v120h-80ZM280-80q-33 0-56.5-23.5T200-160q0-33 23.5-56.5T280-240q33 0 56.5 23.5T360-160q0 33-23.5 56.5T280-80Zm400 0q-33 0-56.5-23.5T600-160q0-33 23.5-56.5T680-240q33 0 56.5 23.5T760-160q0 33-23.5 56.5T680-80ZM40-800v-80h131l170 360h280l156-280h91L692-482q-11 20-29.5 31T622-440H324l-44 80h480v80H280q-45 0-68.5-39t-1.5-79l54-98-144-304H40Z"/></svg>
            </button>
        </div>
    </article>
</template>

<style lang="scss" scoped>
article {
    background: rgba(245, 230, 218, 0.7);
    width: 325px;
    height: 460px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    backdrop-filter: blur(4px);

    img {
        width: 280px;
        height: 280px;
    }

    div {
        h3 {
            font: {
                size: 30px;
            }   
        }

        p {
            font: {
                size: 25px;
            } 
        }
    }

    div {
        button {
            background: none;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #C0A080;
            width: 100px;
            height: 40px;
            border: none;
            border-radius: 20px;
            border-style: solid;
            border-width: 1px;
            cursor: pointer;

            font: {
                size: 16px;
                weight: bold;
            }
            /*width: 50px;
            height: 50px;
            border-radius: 50%;*/

            &:hover {
                box-shadow: 0px 1px 4px black;
            }
        }
    }
}

.more {
    font: {
        size: 12px;
    }
}
</style>