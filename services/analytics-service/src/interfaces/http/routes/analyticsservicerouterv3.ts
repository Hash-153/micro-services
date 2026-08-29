import { Router } from 'express';
import { AnalyticsServiceControllerV3 } from '../controllers/analyticsservicecontrollerv3.js';

export class AnalyticsServiceRouterV3 {
  public static createRouter(controller: AnalyticsServiceControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
