<template>
  <section class="px-4 md:px-8 py-12 max-w-3xl mx-auto mt-18">
    <h2 class="text-2xl font-bold text-[#7D260F] mb-6 font-[Kenia]">
      Notifications
    </h2>

    <div class="flex flex-col gap-4">
      <TwNotification
        v-for="(notif, index) in notifications"
        :key="index"
        :title="notif.title"
        :message="notif.message"
        :time="notif.time"
      />
    </div>
  </section>
</template>

<script setup>

const notifications = [
  {
    title: "Alerte commande",
    message:
      "Votre commande a été bien reçue. Vous serez livré dans quelques heures.",
    time: "17:01"
  },
  {
    title: "Nouvelle promotion",
    message: "Profitez de 20% de réduction sur vos articles préférés.",
    time: "15:45"
  },
  {
    title: "Nouvelle promotion",
    message: "Profitez de 20% de réduction sur vos articles préférés.",
    time: "15:45"
  },
  {
    title: "Nouvelle promotion",
    message: "Profitez de 20% de réduction sur vos articles préférés.",
    time: "15:45"
  },
  {
    title: "Nouvelle promotion",
    message: "Profitez de 20% de réduction sur vos articles préférés.",
    time: "15:45"
  },
  {
    title: "Nouvelle promotion",
    message: "Profitez de 20% de réduction sur vos articles préférés.",
    time: "15:45"
  },
  {
    title: "Nouvelle promotion",
    message: "Profitez de 20% de réduction sur vos articles préférés.",
    time: "15:45"
  }
]
</script>
