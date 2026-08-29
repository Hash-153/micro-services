import { Router } from 'express';
import { InventoryServiceControllerV3 } from '../controllers/inventoryservicecontrollerv3.js';

export class InventoryServiceRouterV3 {
  public static createRouter(controller: InventoryServiceControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
