FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/inventory-service/ services/inventory-service/
RUN npm ci && npm run build --workspace=@novacommerce/inventory-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/inventory-service/dist ./services/inventory-service/dist
COPY --from=builder /app/services/inventory-service/package.json ./services/inventory-service/package.json
EXPOSE 8009
CMD ["node", "services/inventory-service/dist/server.js"]
