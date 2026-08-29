FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/fulfillment-service/ services/fulfillment-service/
RUN npm ci && npm run build --workspace=@novacommerce/fulfillment-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/fulfillment-service/dist ./services/fulfillment-service/dist
COPY --from=builder /app/services/fulfillment-service/package.json ./services/fulfillment-service/package.json
EXPOSE 8006
CMD ["node", "services/fulfillment-service/dist/server.js"]
