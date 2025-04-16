<script setup>
const props = defineProps([
    'link'
])
</script>

<template>
    <NuxtLink :to="link">
        <div class="naviguate">
            <slot></slot>
        </div>
    </NuxtLink>
</template>

<style lang="scss" scoped>
.naviguate {
    color: #935841;
    cursor: pointer;
    font: {
        size: 20px;
        weight: 500;
        family: "Inter";
    }

    &:hover{
        color: #C0A080;
        transition: all 0.3s 0s ease-in-out;
    }
}
</style>