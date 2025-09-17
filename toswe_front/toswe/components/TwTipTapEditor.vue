<template>
  <div class="border rounded-lg bg-white min-h-[220px] p-2">
    <EditorContent :editor="editor" class="prose max-w-none min-h-[180px]" />
    <div class="flex items-center gap-2 mt-2 text-sm text-gray-600">
      <button @click="editor.chain().focus().toggleBold().run()" 
              :class="{'bg-gray-200 font-bold rounded px-2': editor.isActive('bold')}">
        Gras
      </button>
      <button @click="editor.chain().focus().toggleItalic().run()" 
              :class="{'bg-gray-200 italic rounded px-2': editor.isActive('italic')}">
        Italique
      </button>
      <button @click="editor.chain().focus().toggleBulletList().run()" 
              :class="{'bg-gray-200 rounded px-2': editor.isActive('bulletList')}">
        Liste
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, watch } from 'vue'
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'

const props = defineProps<{
  modelValue: string
  placeholder?: string
}>()
const emit = defineEmits(['update:modelValue'])

const editor = ref<Editor>()

editor.value = new Editor({
  extensions: [
    StarterKit,
    Placeholder.configure({
      placeholder: props.placeholder || 'Décris ton produit ici…',
    }),
  ],
  content: props.modelValue,
  onUpdate: ({ editor }) => {
    emit('update:modelValue', editor.getHTML())
  },
})

watch(
  () => props.modelValue,
  (val) => {
    if (editor.value && val !== editor.value.getHTML()) {
      editor.value.commands.setContent(val, false)
    }
  }
)

onBeforeUnmount(() => {
  editor.value?.destroy()
})
</script>

<style scoped>
.prose {
  outline: none;
}
</style>
