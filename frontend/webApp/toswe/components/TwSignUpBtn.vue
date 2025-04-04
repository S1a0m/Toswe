<template>
    <button>S'inscrire</button>
</template>

<style lang="scss" scoped>
button {
    background-color: #2D1B14;
    height: 40px;
    width: 120px;
    color: #F5E6DA;
    border: none;
    box-shadow: 0px 1px 4px black;
    cursor: pointer;
    transition: all 0.5s 0s ease;

    font: {
        size: 18px;
        family: "Inter";
        weight: 500;
    }

    &:hover {
        color: #2D1B14;
        background-color: rgba(245, 230, 218, 0.5);   
    }
}
</style>