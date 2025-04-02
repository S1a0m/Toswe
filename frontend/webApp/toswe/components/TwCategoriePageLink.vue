<script setup>

</script>

<template>
    <NuxtLink>
        <span>
            <slot></slot>
        </span>
    </NuxtLink>
</template>

<style lang="scss" scoped>
span {
    font: {
        size: 22px;
        // weight: 500;
        family: sans-serif;
    }
}
</style>