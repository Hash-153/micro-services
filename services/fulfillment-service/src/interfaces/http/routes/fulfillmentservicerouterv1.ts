import { Router } from 'express';
import { FulfillmentServiceControllerV1 } from '../controllers/fulfillmentservicecontrollerv1.js';

export class FulfillmentServiceRouterV1 {
  public static createRouter(controller: FulfillmentServiceControllerV1): Router {
    const router = Router();

    router.get('/v1/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v1/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v1/items', (req, res) => controller.create(req, res));

    return router;
  }
}
