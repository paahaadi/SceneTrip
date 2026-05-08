# Multi-stage: build the Vite bundle, then serve via nginx.
FROM node:20-slim AS build

WORKDIR /app
COPY package.json ./
RUN npm install --no-audit --no-fund

COPY . .

# VITE_API_BASE must be baked in at build time — Vite inlines env vars.
ARG VITE_API_BASE
ENV VITE_API_BASE=${VITE_API_BASE}
RUN npm run build

# ---- runtime stage ----
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Cloud Run sets $PORT (default 8080); nginx must listen on it.
ENV PORT=8080
CMD ["sh", "-c", "sed -i \"s/\\$PORT/${PORT}/g\" /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
