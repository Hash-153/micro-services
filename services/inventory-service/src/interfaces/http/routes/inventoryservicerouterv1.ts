import { Router } from 'express';
import { InventoryServiceControllerV1 } from '../controllers/inventoryservicecontrollerv1.js';

export class InventoryServiceRouterV1 {
  public static createRouter(controller: InventoryServiceControllerV1): Router {
    const router = Router();

    router.get('/v1/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v1/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v1/items', (req, res) => controller.create(req, res));

    return router;
  }
}
