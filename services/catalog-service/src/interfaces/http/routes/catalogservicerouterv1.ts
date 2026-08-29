import { Router } from 'express';
import { CatalogServiceControllerV1 } from '../controllers/catalogservicecontrollerv1.js';

export class CatalogServiceRouterV1 {
  public static createRouter(controller: CatalogServiceControllerV1): Router {
    const router = Router();

    router.get('/v1/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v1/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v1/items', (req, res) => controller.create(req, res));

    return router;
  }
}
