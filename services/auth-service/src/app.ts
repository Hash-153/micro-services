import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, RequestValidator, AuthMiddleware } from '@novacommerce/core-middleware';
import { InMemoryUserAuthRepository } from './repositories/user-auth.repository.js';
import { TokenService } from './services/token.service.js';
import { AuthService } from './services/auth.service.js';
import { AuthController } from './controllers/auth.controller.js';
import { RegisterUserSchema, LoginUserSchema } from '@novacommerce/core-types';

export function createAuthApp(repo = new InMemoryUserAuthRepository(), tokenService = new TokenService()): Express {
  const app = express();
  const logger = Logger.create('auth-service');
  const authService = new AuthService(repo, tokenService);
  const controller = new AuthController(authService);

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'auth-service' }));

  app.post('/api/v1/auth/register', RequestValidator.validateBody(RegisterUserSchema), controller.register);
  app.post('/api/v1/auth/login', RequestValidator.validateBody(LoginUserSchema), controller.login);
  app.get('/api/v1/auth/me', AuthMiddleware.verifyToken(process.env.JWT_SECRET || 'super_secret_local_jwt_signing_key_min_32_characters_long'), controller.getProfile);

  app.use(ErrorHandlerMiddleware.handle(logger));

  return app;
}
