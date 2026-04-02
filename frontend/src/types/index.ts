// ── Перечисления ─────────────────────────────────────────────────────────────

export type UserRole = 'worker' | 'admin'

// ── Пользователи ─────────────────────────────────────────────────────────────

export interface User {
  id: number
  username: string
  email: string
  role: UserRole
  is_active: boolean
  created_at: string
}

export interface UserRegister {
  username: string
  email: string
  password: string
}

export interface UserLogin {
  username: string
  password: string
}

export interface UserUpdate {
  email?: string
  role?: UserRole
  is_active?: boolean
}

// ── Токены ───────────────────────────────────────────────────────────────────

export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: string
}

// ── Теги ─────────────────────────────────────────────────────────────────────

export interface Tag {
  id: number
  name: string
  color: string
}

export interface TagCreate {
  name: string
  color?: string
}

export interface TagUpdate {
  name?: string
  color?: string
}

// ── Товары ───────────────────────────────────────────────────────────────────

export interface Product {
  id: number
  name: string
  sku: string
  description: string | null
  quantity: number
  price: number
  last_received_at: string | null
  created_at: string
  updated_at: string
  tags: Tag[]
}

export interface ProductCreate {
  name: string
  sku: string
  description?: string
  quantity: number
  price: number
  last_received_at?: string
  tag_ids: number[]
}

export interface ProductUpdate {
  name?: string
  description?: string
  quantity?: number
  price?: number
  last_received_at?: string
  tag_ids?: number[]
}

// ── Ответ со списком и пагинацией ────────────────────────────────────────────

export interface ProductListResponse {
  total: number
  items: Product[]
}

// ── Параметры фильтрации ─────────────────────────────────────────────────────

export interface ProductFilterParams {
  search?: string
  tag_ids?: number[]
  skip?: number
  limit?: number
}

// ── Утилиты ──────────────────────────────────────────────────────────────────

export interface ApiError {
  detail: string
}
