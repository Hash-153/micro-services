import { Request, Response, NextFunction } from 'express';
import { UserProfileService } from '../services/user-profile.service.js';
import { ApiResponse } from '@novacommerce/core-types';

export class UserProfileController {
  private readonly service: UserProfileService;

  constructor(service: UserProfileService) {
    this.service = service;
  }

  public getProfile = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const profile = await this.service.getProfile(userId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: profile
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public updateProfile = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const updated = await this.service.updateProfile(userId, req.body);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: updated
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public listAddresses = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const addresses = await this.service.getAddresses(userId);
      const response: ApiResponse = {
        success: true,
        statusCode: 200,
        data: addresses
      };
      res.status(200).json(response);
    } catch (err) {
      next(err);
    }
  };

  public addAddress = async (req: any, res: Response, next: NextFunction) => {
    try {
      const userId = req.user.sub || req.user.id;
      const address = await this.service.addAddress(userId, req.body);
      const response: ApiResponse = {
        success: true,
        statusCode: 201,
        data: address
      };
      res.status(201).json(response);
    } catch (err) {
      next(err);
    }
  };
}
