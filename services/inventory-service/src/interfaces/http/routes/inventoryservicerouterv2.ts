import { Router } from 'express';
import { InventoryServiceControllerV2 } from '../controllers/inventoryservicecontrollerv2.js';

export class InventoryServiceRouterV2 {
  public static createRouter(controller: InventoryServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
