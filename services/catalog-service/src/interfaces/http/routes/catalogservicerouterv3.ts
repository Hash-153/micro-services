import { Router } from 'express';
import { CatalogServiceControllerV3 } from '../controllers/catalogservicecontrollerv3.js';

export class CatalogServiceRouterV3 {
  public static createRouter(controller: CatalogServiceControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
