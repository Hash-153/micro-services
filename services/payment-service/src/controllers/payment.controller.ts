import { Request, Response, NextFunction } from 'express';
import { PaymentService } from '../services/payment.service.js';
import { ApiResponse, Currency } from '@novacommerce/core-types';

export class PaymentController {
  private readonly service: PaymentService;

  constructor(service: PaymentService) {
    this.service = service;
  }

  public authorize = async (req: any, res: Response, next: NextFunction) => {
    try {
      const { orderId, amountCents, currency } = req.body;
      const userId = req.user?.sub || req.body.userId || 'usr-anon';
      const correlationId = req.headers['x-correlation-id'] as string;
      const payment = await this.service.authorizePayment(orderId, userId, amountCents, currency || Currency.USD, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: payment
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
