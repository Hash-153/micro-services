import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class AuthController {
  private readonly service: AuthService;

  constructor(service: AuthService) {
    this.service = service;
  }

  public register = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const result = await this.service.register(req.body, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: result
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };

  public login = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const result = await this.service.login(req.body, correlationId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: result
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public getProfile = async (req: any, res: Response, next: NextFunction) => {
    try {
      const result = await this.service.getUserById(req.user.sub || req.user.id);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: result
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };
}
