FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/catalog-service/ services/catalog-service/
RUN npm ci && npm run build --workspace=@novacommerce/catalog-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/catalog-service/dist ./services/catalog-service/dist
COPY --from=builder /app/services/catalog-service/package.json ./services/catalog-service/package.json
EXPOSE 8003
CMD ["node", "services/catalog-service/dist/server.js"]
