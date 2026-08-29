import { Router } from 'express';
import { UserServiceControllerV2 } from '../controllers/userservicecontrollerv2.js';

export class UserServiceRouterV2 {
  public static createRouter(controller: UserServiceControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
