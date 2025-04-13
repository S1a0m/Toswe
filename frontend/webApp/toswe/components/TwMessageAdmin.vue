<template>
    <article>
        <!--<img src="/public/images/table-royal.webp" alt="">-->
        <div class="info">
            <p>Bref apercu du message...</p>
            <p>heure d'envoi</p>
            <p>contact de l'emmetteur</p>
        </div>
        <div class="actions">
            <NuxtLink to="/admin/message/read">
                <button type="button">
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#C0A080"><path d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z"/></svg>
                </button>
            </NuxtLink>
            <button type="button">
                <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#C0A080"><path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/></svg>
            </button>
        </div>
    </article>
</template>

<style lang="scss" scoped>
article {
    background: rgba(245, 230, 218, 0.7);
    width: 325px;
    height: 420px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    backdrop-filter: blur(4px);
    transition: all 0.45s 0s ease;

    &:hover {
        transform: translateY(-10px);
        box-shadow: 0px 1px 4px black;
    }

    img {
        width: 280px;
        height: 280px;
        cursor: pointer;
    }

    .info {
        display: flex;
        align-items: center;
        flex-direction: column;
        // justify-content: space-between;
        gap: 20px;
        color: #7D260F;
        margin: 15px 0px 0px 0px ;
        h3 {
            font: {
                size: 25px;
                family: "Lora";
            }   
        }

        p {
            font: {
                family: "Lora";
                weight: 600;
            } 
        }
    }

    .actions {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 10px;
        button {
            background: rgba(245, 230, 218, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #C0A080;
            width: 50px;
            height: 40px;
            border: none;
            border-radius: 20px;
            border-style: solid;
            border-width: 1px;
            cursor: pointer;

            font: {
                size: 16px;
                weight: bold;
                family: "Inter"
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