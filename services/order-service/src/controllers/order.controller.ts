import { Request, Response, NextFunction } from 'express';
import { OrderService } from '../services/order.service.js';
import { ApiResponse, OrderStatus } from '@novacommerce/core-types';

export class OrderController {
  private readonly service: OrderService;

  constructor(service: OrderService) {
    this.service = service;
  }

  public createOrder = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user?.sub || req.body.userId || 'usr-anon';
      const correlationId = req.headers['x-correlation-id'] as string;
      const order = await this.service.createOrder(req.body, userId, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: order
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };

  public getOrder = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const order = await this.service.getOrderById(req.params.id);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: order
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public cancelOrder = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const order = await this.service.updateOrderStatus(req.params.id, OrderStatus.CANCELLED, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: order
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };
}
