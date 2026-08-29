FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/payment-service/ services/payment-service/
RUN npm ci && npm run build --workspace=@novacommerce/payment-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/payment-service/dist ./services/payment-service/dist
COPY --from=builder /app/services/payment-service/package.json ./services/payment-service/package.json
EXPOSE 8005
CMD ["node", "services/payment-service/dist/server.js"]
