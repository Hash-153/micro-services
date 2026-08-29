import { Router } from 'express';
import { ApiGatewayControllerV2 } from '../controllers/apigatewaycontrollerv2.js';

export class ApiGatewayRouterV2 {
  public static createRouter(controller: ApiGatewayControllerV2): Router {
    const router = Router();

    router.get('/v2/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v2/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v2/items', (req, res) => controller.create(req, res));

    return router;
  }
}
