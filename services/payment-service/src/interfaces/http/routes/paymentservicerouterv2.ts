import { Router } from 'express';
import { PaymentServiceControllerV2 } from '../controllers/paymentservicecontrollerv2.js';

export class PaymentServiceRouterV2 {
  public static createRouter(controller: PaymentServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
