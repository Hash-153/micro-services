FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/analytics-service/ services/analytics-service/
RUN npm ci && npm run build --workspace=@novacommerce/analytics-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/analytics-service/dist ./services/analytics-service/dist
COPY --from=builder /app/services/analytics-service/package.json ./services/analytics-service/package.json
EXPOSE 8008
CMD ["node", "services/analytics-service/dist/server.js"]
