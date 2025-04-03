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
        size: 20px;
        // weight: 500;
        family: "Lora";
    }
}
</style>