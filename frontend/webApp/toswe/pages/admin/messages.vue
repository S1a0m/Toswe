<script setup>
definePageMeta({
  layout: 'admin'
})

const messages = ref([]);
</script>

<template>
  <div class="home">
      <main>
        <TwMessageAdmin v-for="message in messages"
        :id="message.id"
        :messagePreview="message.messagePreview"
        :timestamp="message.timestamp"
        :sender="message.sender"/>
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