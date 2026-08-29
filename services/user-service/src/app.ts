import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, AuthMiddleware } from '@novacommerce/core-middleware';
import { InMemoryUserProfileRepository, InMemoryAddressRepository } from './repositories/user-profile.repository.js';
import { UserProfileService } from './services/user-profile.service.js';

export function createUserApp(): Express {
  const app = express();
  const logger = Logger.create('user-service');
  const service = new UserProfileService(new InMemoryUserProfileRepository(), new InMemoryAddressRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'user-service' }));

  const authGuard = AuthMiddleware.verifyToken(process.env.JWT_SECRET || 'super_secret_local_jwt_signing_key_min_32_characters_long');

  app.get('/api/v1/users/profile', authGuard, async (req: any, res, next) => {
    try {
      const profile = await service.getProfile(req.user.sub || req.user.id);
      res.json({ success: true, data: profile });
    } catch (err) {
      next(err);
    }
  });

  app.put('/api/v1/users/profile', authGuard, async (req: any, res, next) => {
    try {
      const profile = await service.updateProfile(req.user.sub || req.user.id, req.body);
      res.json({ success: true, data: profile });
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/v1/users/addresses', authGuard, async (req: any, res, next) => {
    try {
      const addresses = await service.getAddresses(req.user.sub || req.user.id);
      res.json({ success: true, data: addresses });
    } catch (err) {
      next(err);
    }
  });

  app.post('/api/v1/users/addresses', authGuard, async (req: any, res, next) => {
    try {
      const address = await service.addAddress(req.user.sub || req.user.id, req.body);
      res.status(201).json({ success: true, data: address });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
