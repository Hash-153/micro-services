import { Router } from 'express';
import { OrderServiceControllerV2 } from '../controllers/orderservicecontrollerv2.js';

export class OrderServiceRouterV2 {
  public static createRouter(controller: OrderServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
