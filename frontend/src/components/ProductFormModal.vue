<template>
  <!-- Модальное окно добавления / редактирования товара -->
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Подложка -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="close" />

        <!-- Диалог -->
        <div class="relative card w-full max-w-lg max-h-[90vh] overflow-y-auto p-6 z-10">
          <!-- Шапка -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-semibold text-gray-900">
              {{ isEdit ? 'Редактировать товар' : 'Добавить товар' }}
            </h2>
            <button @click="close" class="p-1 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Форма -->
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <!-- Наименование -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Наименование <span class="text-red-500">*</span>
              </label>
              <input v-model="form.name" type="text" class="input-field" placeholder="Название товара" required />
            </div>

            <!-- SKU -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                SKU (артикул) <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.sku"
                type="text"
                class="input-field font-mono"
                placeholder="WH-001"
                :disabled="isEdit"
                :class="{ 'bg-gray-50 cursor-not-allowed': isEdit }"
                required
              />
              <p v-if="isEdit" class="text-xs text-gray-400 mt-1">SKU нельзя изменить после создания</p>
            </div>

            <!-- Описание -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
              <textarea
                v-model="form.description"
                class="input-field resize-none"
                rows="2"
                placeholder="Краткое описание товара..."
              />
            </div>

            <!-- Количество и цена -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Количество <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="form.quantity"
                  type="number"
                  min="0"
                  class="input-field"
                  placeholder="0"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Цена (₽) <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="form.price"
                  type="number"
                  min="0"
                  step="0.01"
                  class="input-field"
                  placeholder="0.00"
                  required
                />
              </div>
            </div>

            <!-- Дата последнего поступления -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Дата последнего поступления</label>
              <input v-model="form.last_received_at" type="date" class="input-field" />
            </div>

            <!-- Мультиселект тегов -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Теги</label>

              <!-- Поиск тегов -->
              <input
                v-model="tagSearch"
                type="text"
                placeholder="Поиск тегов..."
                class="input-field text-sm mb-2"
              />

              <div class="border border-gray-300 rounded-lg p-2 max-h-36 overflow-y-auto space-y-1">
                <label
                  v-for="tag in filteredTags"
                  :key="tag.id"
                  class="flex items-center gap-2 p-1.5 rounded cursor-pointer hover:bg-gray-50"
                >
                  <input
                    type="checkbox"
                    :value="tag.id"
                    v-model="form.tag_ids"
                    class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span
                    class="w-3 h-3 rounded-full flex-shrink-0"
                    :style="{ backgroundColor: tag.color }"
                  />
                  <span class="text-sm text-gray-700">{{ tag.name }}</span>
                </label>
                <p v-if="filteredTags.length === 0" class="text-sm text-gray-400 text-center py-2">
                  Теги не найдены
                </p>
              </div>

              <!-- Выбранные теги -->
              <div v-if="selectedTagObjects.length > 0" class="flex flex-wrap gap-1 mt-2">
                <span
                  v-for="tag in selectedTagObjects"
                  :key="tag.id"
                  class="tag-badge"
                  :style="{ backgroundColor: tag.color }"
                >
                  {{ tag.name }}
                  <button type="button" @click="removeTag(tag.id)" class="ml-1 hover:opacity-75">×</button>
                </span>
              </div>
            </div>

            <!-- Глобальная ошибка -->
            <div v-if="apiError" class="rounded-lg bg-red-50 border border-red-200 p-3">
              <p class="text-sm text-red-700">{{ apiError }}</p>
            </div>

            <!-- Кнопки -->
            <div class="flex justify-end gap-3 pt-2">
              <button type="button" @click="close" class="btn-secondary">Отмена</button>
              <button type="submit" class="btn-primary" :disabled="saving">
                <svg v-if="saving" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                {{ saving ? 'Сохранение...' : isEdit ? 'Сохранить' : 'Добавить' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { tagsApi } from '@/api/tags'
import { productsApi } from '@/api/products'
import type { Product, Tag } from '@/types'

// ── Props & Emits ─────────────────────────────────────────────────────────────

const props = defineProps<{
  isOpen: boolean
  editProduct?: Product | null
}>()

const emit = defineEmits<{
  close: []
  saved: []
}>()

// ── Состояние ────────────────────────────────────────────────────────────────

const allTags = ref<Tag[]>([])
const tagSearch = ref('')
const saving = ref(false)
const apiError = ref<string | null>(null)

const isEdit = computed(() => !!props.editProduct)

const form = ref({
  name: '',
  sku: '',
  description: '',
  quantity: 0,
  price: 0,
  last_received_at: '',
  tag_ids: [] as number[],
})

// ── Заполнение формы при редактировании ──────────────────────────────────────

watch(
  () => props.editProduct,
  (product) => {
    if (product) {
      form.value = {
        name: product.name,
        sku: product.sku,
        description: product.description ?? '',
        quantity: product.quantity,
        price: Number(product.price),
        last_received_at: product.last_received_at
          ? product.last_received_at.split('T')[0]
          : '',
        tag_ids: product.tags.map((t) => t.id),
      }
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

// ── Теги ─────────────────────────────────────────────────────────────────────

const filteredTags = computed(() =>
  tagSearch.value
    ? allTags.value.filter((t) =>
        t.name.toLowerCase().includes(tagSearch.value.toLowerCase())
      )
    : allTags.value
)

const selectedTagObjects = computed(() =>
  allTags.value.filter((t) => form.value.tag_ids.includes(t.id))
)

function removeTag(id: number): void {
  form.value.tag_ids = form.value.tag_ids.filter((x) => x !== id)
}

// ── Сохранение ───────────────────────────────────────────────────────────────

async function handleSubmit(): Promise<void> {
  apiError.value = null
  saving.value = true
  try {
    const payload = {
      ...form.value,
      description: form.value.description || undefined,
      last_received_at: form.value.last_received_at
        ? new Date(form.value.last_received_at).toISOString()
        : undefined,
    }

    if (isEdit.value && props.editProduct) {
      await productsApi.update(props.editProduct.id, payload)
    } else {
      await productsApi.create(payload)
    }
    emit('saved')
    close()
  } catch (err: unknown) {
    const e = err as { response?: { data?: { detail?: string } } }
    apiError.value = e.response?.data?.detail ?? 'Не удалось сохранить товар'
  } finally {
    saving.value = false
  }
}

function close(): void {
  emit('close')
  resetForm()
}

function resetForm(): void {
  form.value = { name: '', sku: '', description: '', quantity: 0, price: 0, last_received_at: '', tag_ids: [] }
  tagSearch.value = ''
  apiError.value = null
}

onMounted(async () => {
  allTags.value = await tagsApi.list()
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
