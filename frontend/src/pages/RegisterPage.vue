<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-indigo-100 flex items-center justify-center p-4">
    <div class="card w-full max-w-md p-8">
      <!-- Логотип -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 bg-primary-600 rounded-2xl mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10" />
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">Регистрация</h1>
        <p class="text-sm text-gray-500 mt-1">Создайте аккаунт в системе управления складом</p>
      </div>

      <!-- Форма -->
      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Логин</label>
          <input
            v-model="form.username"
            type="text"
            autocomplete="username"
            placeholder="Минимум 3 символа"
            class="input-field"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            autocomplete="email"
            placeholder="example@mail.com"
            class="input-field"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            autocomplete="new-password"
            placeholder="Минимум 8 символов"
            class="input-field"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Повторите пароль</label>
          <input
            v-model="form.confirm"
            type="password"
            autocomplete="new-password"
            placeholder="Повторите пароль"
            class="input-field"
            :class="{ 'border-red-500': passwordMismatch }"
            required
          />
          <p v-if="passwordMismatch" class="mt-1 text-xs text-red-600">Пароли не совпадают</p>
        </div>

        <!-- Глобальная ошибка -->
        <div v-if="authStore.error" class="rounded-lg bg-red-50 border border-red-200 p-3">
          <p class="text-sm text-red-700">{{ authStore.error }}</p>
        </div>

        <button
          type="submit"
          class="btn-primary w-full"
          :disabled="authStore.loading || passwordMismatch"
        >
          <svg v-if="authStore.loading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ authStore.loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-gray-600">
        Уже есть аккаунт?
        <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-700">
          Войти
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirm: '',
})

const passwordMismatch = computed(
  () => form.confirm.length > 0 && form.password !== form.confirm
)

async function handleRegister(): Promise<void> {
  if (passwordMismatch.value) return
  try {
    await authStore.register({
      username: form.username,
      email: form.email,
      password: form.password,
    })
    await router.push('/')
  } catch {
    // ошибка записана в authStore.error
  }
}
</script>
