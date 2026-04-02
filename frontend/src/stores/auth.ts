import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import { tokenStorage } from '@/api/client'
import type { User, UserLogin, UserRegister } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  // ── Состояние ──────────────────────────────────────────────────────────────
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // ── Вычисляемые свойства ───────────────────────────────────────────────────
  const isAuthenticated = computed(() => !!user.value && !!tokenStorage.getAccess())
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isWorker = computed(() => user.value?.role === 'worker')

  // ── Действия ──────────────────────────────────────────────────────────────

  /** Инициализация: восстанавливаем пользователя по сохранённому токену */
  async function init(): Promise<void> {
    if (!tokenStorage.getAccess()) return
    try {
      user.value = await authApi.me()
    } catch {
      tokenStorage.clear()
    }
  }

  /** Регистрация */
  async function register(data: UserRegister): Promise<void> {
    loading.value = true
    error.value = null
    try {
      await authApi.register(data)
      // После регистрации — автоматический вход
      await login({ username: data.username, password: data.password })
    } catch (err: unknown) {
      error.value = extractError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /** Вход */
  async function login(data: UserLogin): Promise<void> {
    loading.value = true
    error.value = null
    try {
      await authApi.login(data)
      user.value = await authApi.me()
    } catch (err: unknown) {
      error.value = extractError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /** Выход */
  function logout(): void {
    authApi.logout()
    user.value = null
  }

  // ── Вспомогательная функция ────────────────────────────────────────────────

  function extractError(err: unknown): string {
    if (typeof err === 'object' && err !== null && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      return axiosErr.response?.data?.detail ?? 'Произошла ошибка'
    }
    return 'Произошла ошибка'
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    isWorker,
    init,
    register,
    login,
    logout,
  }
})
