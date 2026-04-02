<template>
  <!-- Боковая панель фильтрации по тегам -->
  <aside class="w-64 flex-shrink-0">
    <div class="card p-4">
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-sm font-semibold text-gray-700 uppercase tracking-wide">Фильтр по тегам</h3>
        <button
          v-if="selected.length > 0"
          @click="clearAll"
          class="text-xs text-primary-600 hover:text-primary-700 font-medium"
        >
          Сбросить
        </button>
      </div>

      <!-- Поиск тегов -->
      <input
        v-model="tagSearch"
        type="text"
        placeholder="Поиск тегов..."
        class="input-field mb-3 text-sm"
      />

      <!-- Список тегов -->
      <div v-if="loading" class="text-sm text-gray-400 text-center py-4">Загрузка...</div>

      <div v-else class="space-y-1 max-h-96 overflow-y-auto pr-1">
        <label
          v-for="tag in filteredTags"
          :key="tag.id"
          class="flex items-center gap-2.5 p-2 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
          :class="{ 'bg-primary-50': isSelected(tag.id) }"
        >
          <input
            type="checkbox"
            :value="tag.id"
            :checked="isSelected(tag.id)"
            @change="toggleTag(tag.id)"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <!-- Цветная метка -->
          <span
            class="w-3 h-3 rounded-full flex-shrink-0"
            :style="{ backgroundColor: tag.color }"
          />
          <span class="text-sm text-gray-700 truncate flex-1">{{ tag.name }}</span>
        </label>

        <p v-if="filteredTags.length === 0" class="text-sm text-gray-400 text-center py-4">
          Теги не найдены
        </p>
      </div>

      <!-- Выбранные теги — краткое резюме -->
      <div v-if="selected.length > 0" class="mt-3 pt-3 border-t border-gray-100">
        <p class="text-xs text-gray-500 mb-1.5">Активно (AND-пересечение):</p>
        <div class="flex flex-wrap gap-1">
          <span
            v-for="tag in selectedTags"
            :key="tag.id"
            class="tag-badge"
            :style="{ backgroundColor: tag.color }"
          >
            {{ tag.name }}
            <button @click="toggleTag(tag.id)" class="ml-0.5 hover:opacity-75">×</button>
          </span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { tagsApi } from '@/api/tags'
import type { Tag } from '@/types'

// ── Props & Emits ─────────────────────────────────────────────────────────────

const props = defineProps<{ modelValue: number[] }>()
const emit = defineEmits<{ 'update:modelValue': [value: number[]] }>()

// ── Состояние ────────────────────────────────────────────────────────────────

const tags = ref<Tag[]>([])
const tagSearch = ref('')
const loading = ref(false)
const selected = computed(() => props.modelValue)

// ── Фильтрация списка тегов по строке поиска ─────────────────────────────────

const filteredTags = computed(() =>
  tagSearch.value
    ? tags.value.filter((t) => t.name.toLowerCase().includes(tagSearch.value.toLowerCase()))
    : tags.value
)

const selectedTags = computed(() =>
  tags.value.filter((t) => selected.value.includes(t.id))
)

// ── Методы ───────────────────────────────────────────────────────────────────

function isSelected(id: number): boolean {
  return selected.value.includes(id)
}

function toggleTag(id: number): void {
  const next = isSelected(id)
    ? selected.value.filter((x) => x !== id)
    : [...selected.value, id]
  emit('update:modelValue', next)
}

function clearAll(): void {
  emit('update:modelValue', [])
}

onMounted(async () => {
  loading.value = true
  try {
    tags.value = await tagsApi.list()
  } finally {
    loading.value = false
  }
})
</script>
