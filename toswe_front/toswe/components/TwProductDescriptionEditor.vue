<script setup>
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const content = ref('')
</script>

<template>
  <div>
    <label class="block mb-2 text-sm font-medium">Description du produit</label><!-- 
      toolbar="full"-->
    <QuillEditor
      v-model:content="content"
      content-type="html"
      theme="snow"
      class="bg-white rounded-lg"
    />
  </div>
</template>
