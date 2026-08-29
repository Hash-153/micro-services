import { Request, Response, NextFunction } from 'express';
import { CatalogService } from '../services/catalog.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class CatalogController {
  private readonly service: CatalogService;

  constructor(service: CatalogService) {
    this.service = service;
  }

  public listProducts = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '20', 10);
      const offset = (page - 1) * limit;
      const { items, total } = await this.service.listProducts(limit, offset);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: items,
        meta: {
          page,
          limit,
          totalItems: total,
          totalPages: Math.ceil(total / limit)
        }
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public getProduct = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const product = await this.service.getProductById(req.params.id);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: product
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public createProduct = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const product = await this.service.createProduct(req.body, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: product
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
