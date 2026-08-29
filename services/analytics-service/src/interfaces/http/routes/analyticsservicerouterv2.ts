import { Router } from 'express';
import { AnalyticsServiceControllerV2 } from '../controllers/analyticsservicecontrollerv2.js';

export class AnalyticsServiceRouterV2 {
  public static createRouter(controller: AnalyticsServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
