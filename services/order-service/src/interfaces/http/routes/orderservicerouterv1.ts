import { Router } from 'express';
import { OrderServiceControllerV1 } from '../controllers/orderservicecontrollerv1.js';

export class OrderServiceRouterV1 {
  public static createRouter(controller: OrderServiceControllerV1): Router {
    const router = Router();

    router.get('/v1/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v1/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v1/items', (req, res) => controller.create(req, res));

    return router;
  }
}
