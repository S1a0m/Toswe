<template>
    <header class="bg-white shadow">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 class="text-3xl font-bold text-gray-900">All sellers</h1>
            <h1 class="text-2xl font-bold text-gray-800">Brands</h1>
        </div>
    </header>
    <div class="sellers-page">
        <h1 class="title">Featured Sellers</h1>
        <div class="sellers-grid">
            <div
                v-for="seller in sellers"
                :key="seller.id"
                class="seller-card glass"
            >
                <img :src="seller.avatar" :alt="seller.name" class="avatar" />
                <h2 class="name">{{ seller.name }}</h2>
                <p class="desc">{{ seller.description }}</p>
                <button class="view-btn">View Profile</button>
            </div>
        </div>
    </div>
</template>

<script setup>
const sellers = [
    {
        id: 1,
        name: "Alice Smith",
        avatar: "https://randomuser.me/api/portraits/women/68.jpg",
        description: "Handmade crafts and unique gifts.",
    },
    {
        id: 2,
        name: "Bob Johnson",
        avatar: "https://randomuser.me/api/portraits/men/45.jpg",
        description: "Vintage collectibles and rare finds.",
    },
    {
        id: 3,
        name: "Carla Gomez",
        avatar: "https://randomuser.me/api/portraits/women/22.jpg",
        description: "Eco-friendly home decor.",
    },
    {
        id: 4,
        name: "David Lee",
        avatar: "https://randomuser.me/api/portraits/men/33.jpg",
        description: "Custom artwork and illustrations.",
    },
];
</script>

<style scoped>
.sellers-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    padding: 2rem;
}
.title {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 2rem;
    color: #222;
    letter-spacing: 1px;
}
.sellers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 2rem;
    max-width: 1100px;
    margin: 0 auto;
}
.seller-card.glass {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.18);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    padding: 2rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: box-shadow 0.2s;
}
.seller-card.glass:hover {
    box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
}
.avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 1rem;
    border: 3px solid rgba(255,255,255,0.5);
}
.name {
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0.5rem 0 0.2rem 0;
    color: #222;
}
.desc {
    font-size: 1rem;
    color: #444;
    text-align: center;
    margin-bottom: 1.2rem;
}
.view-btn {
    background: rgba(255,255,255,0.3);
    border: none;
    border-radius: 1rem;
    padding: 0.5rem 1.5rem;
    color: #222;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
}
.view-btn:hover {
    background: rgba(255,255,255,0.5);
}
</style>