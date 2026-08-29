import { Router } from 'express';
import { AnalyticsServiceControllerV1 } from '../controllers/analyticsservicecontrollerv1.js';

export class AnalyticsServiceRouterV1 {
  public static createRouter(controller: AnalyticsServiceControllerV1): Router {
    const router = Router();

    router.get('/v1/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v1/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v1/items', (req, res) => controller.create(req, res));

    return router;
  }
}
