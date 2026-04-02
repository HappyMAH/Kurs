<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Навигация -->
    <nav class="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-screen-xl mx-auto px-4 sm:px-6 h-16 flex items-center gap-4">
        <router-link to="/" class="flex items-center gap-2 text-gray-500 hover:text-gray-900 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          <span class="text-sm font-medium">Назад</span>
        </router-link>
        <h1 class="text-lg font-bold text-gray-900">Управление пользователями</h1>
      </div>
    </nav>

    <div class="max-w-screen-xl mx-auto px-4 sm:px-6 py-6">
      <div class="card overflow-hidden">
        <!-- Загрузка -->
        <div v-if="loading" class="flex justify-center py-16">
          <svg class="animate-spin w-8 h-8 text-primary-600" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </div>

        <table v-else class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Логин</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Email</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Роль</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Статус</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Создан</th>
              <th class="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase">Действия</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-100">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 group">
              <td class="px-6 py-3 text-sm text-gray-500">{{ user.id }}</td>
              <td class="px-6 py-3 text-sm font-medium text-gray-900">{{ user.username }}</td>
              <td class="px-6 py-3 text-sm text-gray-600">{{ user.email }}</td>
              <td class="px-6 py-3">
                <select
                  :value="user.role"
                  @change="updateRole(user.id, ($event.target as HTMLSelectElement).value as 'worker' | 'admin')"
                  class="text-xs border-gray-200 rounded-md focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="worker">Рабочий</option>
                  <option value="admin">Администратор</option>
                </select>
              </td>
              <td class="px-6 py-3">
                <span
                  class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                  :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                >
                  {{ user.is_active ? 'Активен' : 'Заблокирован' }}
                </span>
              </td>
              <td class="px-6 py-3 text-sm text-gray-500">{{ formatDate(user.created_at) }}</td>
              <td class="px-6 py-3 text-right">
                <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    @click="toggleActive(user)"
                    class="text-xs px-2 py-1 rounded border"
                    :class="user.is_active
                      ? 'border-red-200 text-red-600 hover:bg-red-50'
                      : 'border-green-200 text-green-600 hover:bg-green-50'"
                  >
                    {{ user.is_active ? 'Заблокировать' : 'Разблокировать' }}
                  </button>
                  <button
                    @click="confirmDelete(user)"
                    class="text-xs px-2 py-1 rounded border border-red-200 text-red-600 hover:bg-red-50"
                  >
                    Удалить
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usersApi } from '@/api/users'
import type { User } from '@/types'

const users = ref<User[]>([])
const loading = ref(false)

async function fetchUsers(): Promise<void> {
  loading.value = true
  try {
    users.value = await usersApi.list()
  } finally {
    loading.value = false
  }
}

async function updateRole(id: number, role: 'worker' | 'admin'): Promise<void> {
  await usersApi.update(id, { role })
  await fetchUsers()
}

async function toggleActive(user: User): Promise<void> {
  await usersApi.update(user.id, { is_active: !user.is_active })
  await fetchUsers()
}

async function confirmDelete(user: User): Promise<void> {
  if (confirm(`Удалить пользователя "${user.username}"? Это действие необратимо.`)) {
    await usersApi.remove(user.id)
    await fetchUsers()
  }
}

function formatDate(iso: string): string {
  return new Intl.DateTimeFormat('ru-RU').format(new Date(iso))
}

onMounted(fetchUsers)
</script>
