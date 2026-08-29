import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, RequestValidator } from '@novacommerce/core-middleware';
import { InMemoryProductRepository, InMemoryCategoryRepository } from './repositories/product.repository.js';
import { CatalogService } from './services/catalog.service.js';
import { CreateProductSchema } from '@novacommerce/core-types';

export function createCatalogApp(): Express {
  const app = express();
  const logger = Logger.create('catalog-service');
  const service = new CatalogService(new InMemoryProductRepository(), new InMemoryCategoryRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'catalog-service' }));

  app.get('/api/v1/catalog/products', async (req, res, next) => {
    try {
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '20', 10);
      const offset = (page - 1) * limit;
      const result = await service.listProducts(limit, offset);
      res.json({
        success: true,
        data: result.items,
        meta: { page, limit, totalItems: result.total }
      });
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/v1/catalog/products/:id', async (req, res, next) => {
    try {
      const product = await service.getProductById(req.params.id);
      res.json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  });

  app.post('/api/v1/catalog/products', RequestValidator.validateBody(CreateProductSchema), async (req, res, next) => {
    try {
      const product = await service.createProduct(req.body);
      res.status(201).json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
