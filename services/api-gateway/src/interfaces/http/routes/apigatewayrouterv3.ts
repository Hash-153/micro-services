import { Router } from 'express';
import { ApiGatewayControllerV3 } from '../controllers/apigatewaycontrollerv3.js';

export class ApiGatewayRouterV3 {
  public static createRouter(controller: ApiGatewayControllerV3): Router {
    const router = Router();

    router.get('/v3/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v3/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v3/items', (req, res) => controller.create(req, res));

    return router;
  }
}
