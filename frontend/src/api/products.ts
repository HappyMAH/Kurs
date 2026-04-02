import apiClient from './client'
import type {
  Product,
  ProductCreate,
  ProductFilterParams,
  ProductListResponse,
  ProductUpdate,
} from '@/types'

export const productsApi = {
  /**
   * Список товаров с поиском и фильтрацией по тегам (AND-пересечение).
   * tag_ids: список ID тегов — возвращаются только товары, у которых есть ВСЕ эти теги.
   */
  list: async (params: ProductFilterParams = {}): Promise<ProductListResponse> => {
    const { tag_ids = [], search, skip = 0, limit = 50 } = params

    // URLSearchParams корректно сериализует массив в ?tag_ids=1&tag_ids=2
    const query = new URLSearchParams()
    if (search) query.set('search', search)
    tag_ids.forEach((id) => query.append('tag_ids', String(id)))
    query.set('skip', String(skip))
    query.set('limit', String(limit))

    const res = await apiClient.get<ProductListResponse>(`/products?${query.toString()}`)
    return res.data
  },

  /** Получить один товар по ID */
  get: async (id: number): Promise<Product> => {
    const res = await apiClient.get<Product>(`/products/${id}`)
    return res.data
  },

  /** Создать товар */
  create: async (data: ProductCreate): Promise<Product> => {
    const res = await apiClient.post<Product>('/products', data)
    return res.data
  },

  /** Частичное обновление товара */
  update: async (id: number, data: ProductUpdate): Promise<Product> => {
    const res = await apiClient.patch<Product>(`/products/${id}`, data)
    return res.data
  },

  /** Удалить товар (только admin) */
  remove: async (id: number): Promise<void> => {
    await apiClient.delete(`/products/${id}`)
  },

  /** Экспортировать все товары в CSV (только admin) */
  exportCsv: (): void => {
    const token = localStorage.getItem('access_token')
    const url = `/api/v1/products/export`
    // Создаём временную ссылку для скачивания файла
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'products_export.csv')
    // Добавляем токен через fetch, так как тег <a> не поддерживает заголовки
    fetch(url, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.blob())
      .then((blob) => {
        link.href = URL.createObjectURL(blob)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      })
  },
}
