import { Router } from 'express';
import { PaymentServiceControllerV3 } from '../controllers/paymentservicecontrollerv3.js';

export class PaymentServiceRouterV3 {
  public static createRouter(controller: PaymentServiceControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
