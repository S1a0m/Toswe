<script setup>
definePageMeta({
  layout: 'admin'
})

const messages = ref([]);

async function fetchMessages() {
  // activeCategory.value = category;
  const token = localStorage.getItem("access_token")

  try {
    const response = await fetch(`http://localhost:8000/admin/messages`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la réception.")
    }

    const data = await response.json();
    messages.value = data;

  } catch (error) {
    console.error(error)
    alert("Échec lors de la réception.")
  }
}

onMounted(() => {
  fetchMessages()
})
</script>

<template>
  <div class="home">
      <main>
        <TwMessageAdmin v-for="message in messages"
        :id="message.id_message"
        :messagePreview="message.content"
        :timestamp="message.time_sent"
        :sender="message.mail_or_number"/>
      </main>
    </div>
</template>

<style lang="scss" scoped>

main {
  padding: 40px 80px 80px 80px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}
</style>