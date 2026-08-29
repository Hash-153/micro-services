import { Router } from 'express';
import { FulfillmentServiceControllerV2 } from '../controllers/fulfillmentservicecontrollerv2.js';

export class FulfillmentServiceRouterV2 {
  public static createRouter(controller: FulfillmentServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
