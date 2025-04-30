<script setup>
definePageMeta({
  layout: 'admin'
})

const notifications = ref([]);

async function fetchNotification() {
  // activeCategory.value = category;
  const token = localStorage.getItem("access_token")

  try {
    const response = await fetch(`http://localhost:8000/admin/notifications`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la réception.")
    }

    const data = await response.json();
    articles.value = data;

  } catch (error) {
    console.error(error)
    alert("Échec lors de la réception.")
  }
}
</script>

<template>
  <div class="home">
      <header>
      </header>
      <main>
        <TwNotificationAdmin v-for="notification in notifications"
        :id="notification.id"
        :title="notification.title"
        :messagePreview="notification.messagePreview"
        :status="notification.status"
        />
      </main>
    </div>
</template>

<style lang="scss" scoped>


header {
  display: flex;
  padding: 30px;
  align-items: center;
  justify-content: space-between;

  .shopping-cart {
    background: rgba(245, 230, 218, 0.3);
    width: 72px;
    height: 50px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);
    color: #C0A080;

    font: {
      weight: bold;
      size: 18px;
    }
  }

  nav {
    background: rgba(245, 230, 218, 0.3);
    width: 92vw;
    height: 50px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);

    ul {
      list-style-type: none;
      display: flex;
      // gap: 10px;
      justify-content: space-between;
      align-items: center;
      width: 90%;

      li {
        cursor: pointer;

        &:hover {
          color: #C0A080;
          text-decoration: underline;
          text-decoration-thickness: 2px;
          text-underline-offset: 8px;
        }
      }

      .active-categorie-page {
        color: #C0A080;
        text-decoration: underline;
        text-decoration-thickness: 2px;
        text-underline-offset: 8px;
      }
    }
  }
}

main {
  padding: 40px 80px 80px 80px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}
</style>