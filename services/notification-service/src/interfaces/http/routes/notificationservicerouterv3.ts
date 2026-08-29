import { Router } from 'express';
import { NotificationServiceControllerV3 } from '../controllers/notificationservicecontrollerv3.js';

export class NotificationServiceRouterV3 {
  public static createRouter(controller: NotificationServiceControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
