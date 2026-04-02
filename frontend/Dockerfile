FROM node:20-alpine AS builder

WORKDIR /app

# Устанавливаем зависимости
COPY package*.json ./
RUN npm install

# Копируем исходники и собираем
COPY . .
RUN npm run build

# ── Продакшн-образ: отдаём статику через nginx ────────────────────────────────
FROM nginx:1.27-alpine AS production

# Копируем собранный фронтенд
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx будет настроен снаружи (volume или отдельный конфиг)
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
