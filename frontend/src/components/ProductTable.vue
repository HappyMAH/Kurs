<template>
  <div class="overflow-x-auto">
    <!-- Пустое состояние -->
    <div v-if="!loading && products.length === 0" class="text-center py-16">
      <svg class="mx-auto w-12 h-12 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0H4" />
      </svg>
      <p class="text-gray-500 font-medium">Товары не найдены</p>
      <p class="text-sm text-gray-400 mt-1">Попробуйте изменить фильтры или добавьте первый товар</p>
    </div>

    <table v-else class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="th-cell">Наименование</th>
          <th class="th-cell">Артикул (SKU)</th>
          <th class="th-cell text-right">Кол-во</th>
          <th class="th-cell text-right">Цена (₽)</th>
          <th class="th-cell">Последнее поступление</th>
          <th class="th-cell">Теги</th>
          <th class="th-cell text-right">Действия</th>
        </tr>
      </thead>

      <tbody class="bg-white divide-y divide-gray-100">
        <!-- Скелетон загрузки -->
        <template v-if="loading">
          <tr v-for="n in 8" :key="n" class="animate-pulse">
            <td class="td-cell"><div class="h-4 bg-gray-200 rounded w-3/4" /></td>
            <td class="td-cell"><div class="h-4 bg-gray-200 rounded w-1/2" /></td>
            <td class="td-cell"><div class="h-4 bg-gray-200 rounded w-12 ml-auto" /></td>
            <td class="td-cell"><div class="h-4 bg-gray-200 rounded w-16 ml-auto" /></td>
            <td class="td-cell"><div class="h-4 bg-gray-200 rounded w-24" /></td>
            <td class="td-cell"><div class="h-4 bg-gray-200 rounded w-32" /></td>
            <td class="td-cell"><div class="h-4 bg-gray-200 rounded w-16 ml-auto" /></td>
          </tr>
        </template>

        <!-- Данные -->
        <tr
          v-else
          v-for="product in products"
          :key="product.id"
          class="hover:bg-gray-50 transition-colors group"
        >
          <td class="td-cell">
            <div class="font-medium text-gray-900">{{ product.name }}</div>
            <div v-if="product.description" class="text-xs text-gray-400 truncate max-w-xs mt-0.5">
              {{ product.description }}
            </div>
          </td>
          <td class="td-cell">
            <code class="text-xs bg-gray-100 px-2 py-0.5 rounded font-mono">{{ product.sku }}</code>
          </td>
          <td class="td-cell text-right">
            <span
              class="font-semibold"
              :class="product.quantity === 0 ? 'text-red-600' : product.quantity < 10 ? 'text-amber-600' : 'text-gray-900'"
            >
              {{ product.quantity }}
            </span>
          </td>
          <td class="td-cell text-right font-medium text-gray-900">
            {{ formatPrice(product.price) }}
          </td>
          <td class="td-cell text-sm text-gray-500">
            {{ product.last_received_at ? formatDate(product.last_received_at) : '—' }}
          </td>
          <td class="td-cell">
            <div class="flex flex-wrap gap-1">
              <span
                v-for="tag in product.tags"
                :key="tag.id"
                class="tag-badge"
                :style="{ backgroundColor: tag.color }"
                :title="tag.name"
              >
                {{ tag.name }}
              </span>
              <span v-if="product.tags.length === 0" class="text-xs text-gray-400">—</span>
            </div>
          </td>
          <td class="td-cell text-right">
            <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                @click="emit('edit', product)"
                class="p-1.5 text-gray-400 hover:text-primary-600 rounded-md hover:bg-primary-50 transition-colors"
                title="Редактировать"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                v-if="isAdmin"
                @click="confirmDelete(product)"
                class="p-1.5 text-gray-400 hover:text-red-600 rounded-md hover:bg-red-50 transition-colors"
                title="Удалить"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Пагинация -->
    <div v-if="total > 0" class="flex items-center justify-between px-4 py-3 border-t border-gray-200 bg-white">
      <p class="text-sm text-gray-600">
        Показано <span class="font-medium">{{ products.length }}</span> из
        <span class="font-medium">{{ total }}</span> товаров
      </p>
      <div class="flex gap-2">
        <button
          @click="emit('prev')"
          :disabled="!hasPrev"
          class="btn-secondary py-1.5 px-3 text-xs disabled:opacity-40"
        >
          ← Предыдущая
        </button>
        <button
          @click="emit('next')"
          :disabled="!hasNext"
          class="btn-secondary py-1.5 px-3 text-xs disabled:opacity-40"
        >
          Следующая →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Product } from '@/types'

// ── Props ─────────────────────────────────────────────────────────────────────

const props = defineProps<{
  products: Product[]
  loading: boolean
  total: number
  skip: number
  limit: number
  isAdmin: boolean
}>()

const emit = defineEmits<{
  edit: [product: Product]
  delete: [product: Product]
  next: []
  prev: []
}>()

// ── Вычисляемые свойства ─────────────────────────────────────────────────────

const hasPrev = computed(() => props.skip > 0)
const hasNext = computed(() => props.skip + props.limit < props.total)

// ── Утилиты ──────────────────────────────────────────────────────────────────

function formatPrice(price: number): string {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 2,
  }).format(price)
}

function formatDate(iso: string): string {
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(new Date(iso))
}

function confirmDelete(product: Product): void {
  if (confirm(`Удалить товар "${product.name}"?`)) {
    emit('delete', product)
  }
}
</script>

<style scoped>
.th-cell {
  @apply px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider;
}
.td-cell {
  @apply px-4 py-3 text-sm;
}
</style>


