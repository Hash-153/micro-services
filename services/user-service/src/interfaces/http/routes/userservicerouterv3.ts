import { Router } from 'express';
import { UserServiceControllerV3 } from '../controllers/userservicecontrollerv3.js';

export class UserServiceRouterV3 {
  public static createRouter(controller: UserServiceControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
