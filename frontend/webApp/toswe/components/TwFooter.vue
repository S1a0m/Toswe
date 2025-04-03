<template>
    <div class="footer">
        <div class="tw-location">
            <img src="" alt="">
            <svg xmlns="http://www.w3.org/2000/svg" height="30px" viewBox="0 -960 960 960" width="25px" fill="#2D1B14"><path d="M480-480q33 0 56.5-23.5T560-560q0-33-23.5-56.5T480-640q-33 0-56.5 23.5T400-560q0 33 23.5 56.5T480-480Zm0 294q122-112 181-203.5T720-552q0-109-69.5-178.5T480-800q-101 0-170.5 69.5T240-552q0 71 59 162.5T480-186Zm0 106Q319-217 239.5-334.5T160-552q0-150 96.5-239T480-880q127 0 223.5 89T800-552q0 100-79.5 217.5T480-80Zm0-480Z"/></svg>
            Abomey-Calavi
        </div>
        <address>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" height="100px" viewBox="0 -960 960 960" width="100px" fill="#2D1B14"><path d="M798-120q-125 0-247-54.5T329-329Q229-429 174.5-551T120-798q0-18 12-30t30-12h162q14 0 25 9.5t13 22.5l26 140q2 16-1 27t-11 19l-97 98q20 37 47.5 71.5T387-386q31 31 65 57.5t72 48.5l94-94q9-9 23.5-13.5T670-390l138 28q14 4 23 14.5t9 23.5v162q0 18-12 30t-30 12ZM241-600l66-66-17-94h-89q5 41 14 81t26 79Zm358 358q39 17 79.5 27t81.5 13v-88l-94-19-67 67ZM241-600Zm358 358Z"/></svg>
                <div>
                    <p>Whatsapp - Appel direct</p>
                    <p>+229 015 678 7899</p>
                    <p>+229 010 870 4532</p>
                </div>
            </div>
            <div>
                <p><span class="ic facebook">F</span>acebook</p>
                <p>Tôswè Afriica</p>
            </div>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" height="100px" viewBox="0 -960 960 960" width="100px" fill="#2D1B14"><path d="M160-160q-33 0-56.5-23.5T80-240v-480q0-33 23.5-56.5T160-800h640q33 0 56.5 23.5T880-720v480q0 33-23.5 56.5T800-160H160Zm320-280L160-640v400h640v-400L480-440Zm0-80 320-200H160l320 200ZM160-640v-80 480-400Z"/></svg>
                <div>
                    <p>toswe.africa@gmail.com</p>
                    <p>assistance@toswe.africa</p>
                </div>
            </div>
            <div>
                <p><span class="ic tiktok">T</span>iktok</p>
                <p>Tôswè Africa</p>
            </div>
        </address>
        <div class="tw-rules">
            <NuxtLink to="/rules">
                <span class="rules">Conditions générales de ventes · Politiques de confidentialités · Cookies</span>
            </NuxtLink>
            <p>© 2024 Copyright - Tôswè Africa</p>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.footer {
    background-color: rgba(245, 230, 218, 0.3);
}

.tw-location {
    color: #2D1B14;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 10px;
    background: rgba(45, 27, 20, 0.2);
    height: 44px;
    

    font: {
        size: 16px;
        family: "Inter";
    }
}


address {
    display: flex;
    justify-content: space-around;
    font-size: 16px;
    font-family: "Inter";

    & div {
        display: flex;
        justify-content: center;
        align-items: center;

        div {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
    }
}

.ic {
    color: rgba(45, 27, 20, 1);

    font: {
        size: 100px;
        weight: 800;
    }
}

.tw-rules {
    color: #2D1B14;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: rgba(45, 27, 20, 0.2);
    padding: 20px;
    gap: 5px;

    font: {
        size: 14px;
    }
}

a {
    color: #2D1B14;
    text-decoration: none;
}

.rules:hover {
    text-decoration: underline;
    cursor: pointer;
}
</style>