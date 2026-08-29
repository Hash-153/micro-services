import { Request, Response, NextFunction } from 'express';
import { FulfillmentService } from '../services/fulfillment.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class FulfillmentController {
  private readonly service: FulfillmentService;

  constructor(service: FulfillmentService) {
    this.service = service;
  }

  public createShipment = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { orderId, destinationAddress, carrier } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const shipment = await this.service.createShipment(orderId, destinationAddress || {}, carrier, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: shipment
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
