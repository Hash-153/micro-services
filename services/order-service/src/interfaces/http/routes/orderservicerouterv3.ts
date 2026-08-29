import { Router } from 'express';
import { OrderServiceControllerV3 } from '../controllers/orderservicecontrollerv3.js';

export class OrderServiceRouterV3 {
  public static createRouter(controller: OrderServiceControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
