import { Router } from 'express';
import { NotificationServiceControllerV2 } from '../controllers/notificationservicecontrollerv2.js';

export class NotificationServiceRouterV2 {
  public static createRouter(controller: NotificationServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
