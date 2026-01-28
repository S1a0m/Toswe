<!-- pages/add.vue -->
<template>
    <section class="px-4 md:px-8 py-12 max-w-6xl mx-auto">
        <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">{{ route === "/edit" ? "Ajouter un nouveau produit" : "Modifier le produit" }}</h2>
        <TwProductDescriptionEditor mode="update"/>
    </section>
</template>

<script lang="ts">
const route = useRoute()
</script>