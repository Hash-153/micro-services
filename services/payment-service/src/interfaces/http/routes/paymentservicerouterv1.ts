import { Router } from 'express';
import { PaymentServiceControllerV1 } from '../controllers/paymentservicecontrollerv1.js';

export class PaymentServiceRouterV1 {
  public static createRouter(controller: PaymentServiceControllerV1): Router {
    const router = Router();

    router.get('/v1/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v1/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v1/items', (req, res) => controller.create(req, res));

    return router;
  }
}
