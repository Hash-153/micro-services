import { Router } from 'express';
import { CatalogServiceControllerV2 } from '../controllers/catalogservicecontrollerv2.js';

export class CatalogServiceRouterV2 {
  public static createRouter(controller: CatalogServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
