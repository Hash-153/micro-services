import { Request, Response, NextFunction } from 'express';
import { MfaService } from '../services/mfa.service.js';
import { UserAuthRepository } from '../repositories/user-auth.repository.js';
import { ApiResponse, ApiErrorResponse } from '@novacommerce/core-types';

export class MfaController {
  private mfaService: MfaService;
  private userRepo: UserAuthRepository;

  constructor(mfaService: MfaService, userRepo: UserAuthRepository) {
    this.mfaService = mfaService;
    this.userRepo = userRepo;
  }

  public enroll = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = (req as any).user;
      const secret = this.mfaService.generateMfaSecret();
      const qrCodeUrl = `otpauth://totp/NovaCommerce:${user.email}?secret=${secret}&issuer=NovaCommerce`;

      const response: ApiResponse<{ secret: string; qrCodeUrl: string }> = {
        success: true,
        statusCode: 200,
        data: { secret, qrCodeUrl }
      };
      res.json(response);
    } catch (error) {
      next(error);
    }
  };

  public verify = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = (req as any).user;
      const { code, secret } = req.body;

      if (!code || !secret) {
        return res.status(400).json({
          success: false,
          statusCode: 400,
          error: { code: 'ERR_VALIDATION', message: 'MFA verification code and secret are required.', timestamp: new Date().toISOString() }
        });
      }

      const isValid = this.mfaService.verifyTotp(code, secret);
      if (!isValid) {
        return res.status(400).json({
          success: false,
          statusCode: 400,
          error: { code: 'ERR_INVALID_MFA_CODE', message: 'Invalid or expired 6-digit TOTP code.', timestamp: new Date().toISOString() }
        });
      }

      await this.userRepo.update(user.id, { isMfaEnabled: true, mfaSecret: secret });

      res.json({
        success: true,
        statusCode: 200,
        data: { message: 'Two-factor authentication successfully enabled.' }
      });
    } catch (error) {
      next(error);
    }
  };
}
