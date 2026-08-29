import { Request, Response, NextFunction } from 'express';
import { InventoryService } from '../services/inventory.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class InventoryController {
  private readonly service: InventoryService;

  constructor(service: InventoryService) {
    this.service = service;
  }

  public setStock = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { sku, warehouseId, quantity } = req.body;
      const stock = await this.service.setStock(sku, warehouseId || 'WH-MAIN-01', quantity);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: stock
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public reserve = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { orderId, sku, quantity } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const reservation = await this.service.reserveStock(orderId, sku, quantity, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: reservation
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };

  public release = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { orderId } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      await this.service.releaseReservation(orderId, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: { message: `Released reservations for order ${orderId}` }
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };
}
