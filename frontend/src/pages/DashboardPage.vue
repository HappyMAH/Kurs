<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ── Навигационная панель ─────────────────────────────────────────────── -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-screen-xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <!-- Логотип -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10" />
            </svg>
          </div>
          <span class="font-bold text-gray-900 text-lg">Умный Склад</span>
        </div>

        <!-- Навигация -->
        <div class="flex items-center gap-4">
          <router-link
            v-if="authStore.isAdmin"
            to="/users"
            class="text-sm text-gray-600 hover:text-primary-600 font-medium transition-colors"
          >
            Пользователи
          </router-link>

          <!-- Кнопка экспорта CSV (только admin) -->
          <button
            v-if="authStore.isAdmin"
            @click="exportCsv"
            class="btn-secondary py-1.5 text-xs gap-1.5"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Экспорт CSV
          </button>

          <!-- Пользователь -->
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span class="text-sm font-semibold text-primary-700">
                {{ authStore.user?.username[0].toUpperCase() }}
              </span>
            </div>
            <div class="hidden sm:block">
              <p class="text-sm font-medium text-gray-900 leading-tight">{{ authStore.user?.username }}</p>
              <p class="text-xs text-gray-500 leading-tight">
                {{ authStore.user?.role === 'admin' ? 'Администратор' : 'Рабочий' }}
              </p>
            </div>
            <button @click="handleLogout" class="ml-2 p-1.5 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors" title="Выйти">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- ── Тело страницы ────────────────────────────────────────────────────── -->
    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 py-6">

      <!-- Заголовок + кнопка добавления -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Склад</h1>
          <p class="text-sm text-gray-500 mt-0.5">
            Всего товаров: <span class="font-semibold text-gray-800">{{ total }}</span>
          </p>
        </div>
        <button @click="openCreate" class="btn-primary gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Добавить товар
        </button>
      </div>

      <!-- Строка поиска -->
      <div class="card p-4 mb-6">
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            v-model="search"
            type="search"
            placeholder="Поиск по названию или SKU..."
            class="input-field pl-10"
          />
        </div>
      </div>

      <!-- Основной контент: фильтры + таблица -->
      <div class="flex gap-6">

        <!-- Боковая панель с фильтрами тегов -->
        <TagFilter v-model="selectedTagIds" />

        <!-- Таблица товаров -->
        <div class="flex-1 card overflow-hidden">
          <ProductTable
            :products="products"
            :loading="loading"
            :total="total"
            :skip="skip"
            :limit="limit"
            :is-admin="authStore.isAdmin"
            @edit="openEdit"
            @delete="handleDelete"
            @next="nextPage"
            @prev="prevPage"
          />
        </div>
      </div>
    </div>

    <!-- ── Модальное окно добавления / редактирования ──────────────────────── -->
    <ProductFormModal
      :is-open="modalOpen"
      :edit-product="editingProduct"
      @close="modalOpen = false"
      @saved="fetchProducts"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { productsApi } from '@/api/products'
import TagFilter from '@/components/TagFilter.vue'
import ProductTable from '@/components/ProductTable.vue'
import ProductFormModal from '@/components/ProductFormModal.vue'
import type { Product } from '@/types'

const router = useRouter()
const authStore = useAuthStore()

// ── Состояние ────────────────────────────────────────────────────────────────

const products = ref<Product[]>([])
const total = ref(0)
const loading = ref(false)

// Поиск и фильтрация
const search = ref('')
const selectedTagIds = ref<number[]>([])

// Пагинация
const skip = ref(0)
const limit = ref(50)

// Модальное окно
const modalOpen = ref(false)
const editingProduct = ref<Product | null>(null)

// ── Загрузка данных ──────────────────────────────────────────────────────────

async function fetchProducts(): Promise<void> {
  loading.value = true
  try {
    const result = await productsApi.list({
      search: search.value || undefined,
      tag_ids: selectedTagIds.value,
      skip: skip.value,
      limit: limit.value,
    })
    products.value = result.items
    total.value = result.total
  } finally {
    loading.value = false
  }
}

// Сбрасываем пагинацию при изменении фильтров
watch([search, selectedTagIds], () => {
  skip.value = 0
  fetchProducts()
})

// ── Пагинация ─────────────────────────────────────────────────────────────────

function nextPage(): void {
  skip.value += limit.value
  fetchProducts()
}

function prevPage(): void {
  skip.value = Math.max(0, skip.value - limit.value)
  fetchProducts()
}

// ── CRUD-действия ─────────────────────────────────────────────────────────────

function openCreate(): void {
  editingProduct.value = null
  modalOpen.value = true
}

function openEdit(product: Product): void {
  editingProduct.value = product
  modalOpen.value = true
}

async function handleDelete(product: Product): Promise<void> {
  try {
    await productsApi.remove(product.id)
    await fetchProducts()
  } catch (e) {
    alert('Не удалось удалить товар')
  }
}

function exportCsv(): void {
  productsApi.exportCsv()
}

function handleLogout(): void {
  authStore.logout()
  router.push('/login')
}

// ── Инициализация ─────────────────────────────────────────────────────────────

onMounted(fetchProducts)
</script>
