import apiClient from './client'
import type { Tag, TagCreate, TagUpdate } from '@/types'

export const tagsApi = {
  /** Получить все теги */
  list: async (): Promise<Tag[]> => {
    const res = await apiClient.get<Tag[]>('/tags')
    return res.data
  },

  /** Создать новый тег */
  create: async (data: TagCreate): Promise<Tag> => {
    const res = await apiClient.post<Tag>('/tags', data)
    return res.data
  },

  /** Обновить тег (только admin) */
  update: async (id: number, data: TagUpdate): Promise<Tag> => {
    const res = await apiClient.patch<Tag>(`/tags/${id}`, data)
    return res.data
  },

  /** Удалить тег (только admin) */
  remove: async (id: number): Promise<void> => {
    await apiClient.delete(`/tags/${id}`)
  },
}
