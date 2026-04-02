import apiClient from './client'
import type { User, UserUpdate } from '@/types'

export const usersApi = {
  /** Получить список всех пользователей (только admin) */
  list: async (skip = 0, limit = 50): Promise<User[]> => {
    const res = await apiClient.get<User[]>(`/users?skip=${skip}&limit=${limit}`)
    return res.data
  },

  /** Получить пользователя по ID (только admin) */
  get: async (id: number): Promise<User> => {
    const res = await apiClient.get<User>(`/users/${id}`)
    return res.data
  },

  /** Изменить роль / статус пользователя (только admin) */
  update: async (id: number, data: UserUpdate): Promise<User> => {
    const res = await apiClient.patch<User>(`/users/${id}`, data)
    return res.data
  },

  /** Удалить пользователя (только admin) */
  remove: async (id: number): Promise<void> => {
    await apiClient.delete(`/users/${id}`)
  },
}
