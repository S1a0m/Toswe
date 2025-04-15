<template>
    <button>
        Se deconnecter
        <svg xmlns="http://www.w3.org/2000/svg" height="25px" viewBox="0 -960 960 960" width="25px" fill="#2D1B14"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h280v80H200Zm440-160-55-58 102-102H360v-80h327L585-622l55-58 200 200-200 200Z"/></svg>
    </button>
</template>

<style lang="scss" scoped>
button {
    // background-color: rgba(245, 230, 218, 0.5);
    background: none;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 40px;
    padding: 5px;
    //width: 151px;
    color: #2D1B14;
    border: none;
    box-shadow: 0px 2px 0px #2D1B14;
    cursor: pointer;
    transition: all 0.2s 0s ease;

    font: {
        size: 18px;
        family: "Inter";
        weight: 500;
    }

    &:hover {
        box-shadow: 0px 1px 4px black;     
    }
}
</style>