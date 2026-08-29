import { Router } from 'express';
import { ApiGatewayControllerV1 } from '../controllers/apigatewaycontrollerv1.js';

export class ApiGatewayRouterV1 {
  public static createRouter(controller: ApiGatewayControllerV1): Router {
    const router = Router();

    router.get('/v1/items/:id', (req, res) => controller.getById(req, res));
    router.get('/v1/items', (req, res) => controller.listByTenant(req, res));
    router.post('/v1/items', (req, res) => controller.create(req, res));

    return router;
  }
}
