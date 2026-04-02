import apiClient, { tokenStorage } from './client'
import type { TokenPair, User, UserLogin, UserRegister } from '@/types'

export const authApi = {
  /** Регистрация нового пользователя */
  register: async (data: UserRegister): Promise<User> => {
    const res = await apiClient.post<User>('/auth/register', data)
    return res.data
  },

  /** Вход по логину и паролю */
  login: async (data: UserLogin): Promise<TokenPair> => {
    const res = await apiClient.post<TokenPair>('/auth/login', data)
    tokenStorage.setTokens(res.data.access_token, res.data.refresh_token)
    return res.data
  },

  /** Обновление пары токенов */
  refresh: async (): Promise<TokenPair> => {
    const refreshToken = tokenStorage.getRefresh()
    const res = await apiClient.post<TokenPair>('/auth/refresh', {
      refresh_token: refreshToken,
    })
    tokenStorage.setTokens(res.data.access_token, res.data.refresh_token)
    return res.data
  },

  /** Получение данных текущего пользователя */
  me: async (): Promise<User> => {
    const res = await apiClient.get<User>('/auth/me')
    return res.data
  },

  /** Выход из системы */
  logout: (): void => {
    tokenStorage.clear()
  },
}
