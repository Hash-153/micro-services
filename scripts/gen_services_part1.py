import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_api_gateway():
    svc_dir = "services/api-gateway"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/api-gateway",
  "version": "1.0.0",
  "description": "NovaCommerce Enterprise API Gateway with reverse proxy and rate limiting",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "express": "^4.19.2",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "compression": "^1.7.4",
    "http-proxy-middleware": "^3.0.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/cors": "^2.8.17",
    "@types/compression": "^1.7.5",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/api-gateway/ services/api-gateway/
RUN npm ci && npm run build --workspace=@novacommerce/api-gateway

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/api-gateway/dist ./services/api-gateway/dist
COPY --from=builder /app/services/api-gateway/package.json ./services/api-gateway/package.json
EXPOSE 8000
CMD ["node", "services/api-gateway/dist/server.js"]
""")

    write_file(f"{svc_dir}/src/config/gateway.config.ts", """export interface GatewayRoute {
  pathPrefix: string;
  targetUrl: string;
  authRequired: boolean;
  rateLimitMax: number;
}

export const GatewayConfig = {
  port: parseInt(process.env.GATEWAY_PORT || '8000', 10),
  host: process.env.GATEWAY_HOST || '0.0.0.0',
  jwtSecret: process.env.JWT_SECRET || 'super_secret_local_jwt_signing_key_min_32_characters_long',
  routes: [
    {
      pathPrefix: '/api/v1/auth',
      targetUrl: process.env.AUTH_SERVICE_URL || 'http://localhost:8001',
      authRequired: false,
      rateLimitMax: 100
    },
    {
      pathPrefix: '/api/v1/users',
      targetUrl: process.env.USER_SERVICE_URL || 'http://localhost:8002',
      authRequired: true,
      rateLimitMax: 200
    },
    {
      pathPrefix: '/api/v1/catalog',
      targetUrl: process.env.CATALOG_SERVICE_URL || 'http://localhost:8003',
      authRequired: false,
      rateLimitMax: 500
    },
    {
      pathPrefix: '/api/v1/orders',
      targetUrl: process.env.ORDER_SERVICE_URL || 'http://localhost:8004',
      authRequired: true,
      rateLimitMax: 150
    },
    {
      pathPrefix: '/api/v1/payments',
      targetUrl: process.env.PAYMENT_SERVICE_URL || 'http://localhost:8005',
      authRequired: true,
      rateLimitMax: 100
    },
    {
      pathPrefix: '/api/v1/fulfillment',
      targetUrl: process.env.FULFILLMENT_SERVICE_URL || 'http://localhost:8006',
      authRequired: true,
      rateLimitMax: 150
    },
    {
      pathPrefix: '/api/v1/notifications',
      targetUrl: process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:8007',
      authRequired: true,
      rateLimitMax: 100
    },
    {
      pathPrefix: '/api/v1/analytics',
      targetUrl: process.env.ANALYTICS_SERVICE_URL || 'http://localhost:8008',
      authRequired: true,
      rateLimitMax: 300
    },
    {
      pathPrefix: '/api/v1/inventory',
      targetUrl: process.env.INVENTORY_SERVICE_URL || 'http://localhost:8009',
      authRequired: true,
      rateLimitMax: 300
    }
  ]
};
""")

    write_file(f"{svc_dir}/src/app.ts", """import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, SlidingWindowRateLimiter } from '@novacommerce/core-middleware';
import { GatewayConfig } from './config/gateway.config.js';
import { randomUUID } from 'crypto';

export function createGatewayApp(): Express {
  const app = express();
  const logger = Logger.create('api-gateway');

  app.use(helmet());
  app.use(cors({ origin: '*' }));
  app.use(compression());
  app.use(express.json());

  // Correlation ID middleware
  app.use((req: Request, res: Response, next: NextFunction) => {
    const correlationId = (req.headers['x-correlation-id'] as string) || randomUUID();
    req.headers['x-correlation-id'] = correlationId;
    res.setHeader('x-correlation-id', correlationId);
    next();
  });

  // Global rate limiter
  const globalLimiter = new SlidingWindowRateLimiter(60000, 1000);
  app.use(globalLimiter.middleware());

  // Health and Readiness probes
  app.get('/health', (req: Request, res: Response) => {
    res.json({
      status: 'UP',
      service: 'api-gateway',
      timestamp: new Date().toISOString(),
      routesCount: GatewayConfig.routes.length
    });
  });

  app.get('/routes', (req: Request, res: Response) => {
    res.json({
      routes: GatewayConfig.routes.map(r => ({
        path: r.pathPrefix,
        authRequired: r.authRequired,
        rateLimit: r.rateLimitMax
      }))
    });
  });

  // Error handling
  app.use(ErrorHandlerMiddleware.handle(logger));

  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createGatewayApp } from './app.js';
import { GatewayConfig } from './config/gateway.config.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('api-gateway');
const app = createGatewayApp();

const server = app.listen(GatewayConfig.port, GatewayConfig.host, () => {
  logger.info(`NovaCommerce API Gateway listening on http://${GatewayConfig.host}:${GatewayConfig.port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down API Gateway gracefully...');
  server.close(() => {
    logger.info('API Gateway closed successfully.');
    process.exit(0);
  });
});
""")

    write_file(f"{svc_dir}/tests/gateway.test.ts", """import request from 'supertest';
import { createGatewayApp } from '../src/app.js';

describe('API Gateway Suite', () => {
  const app = createGatewayApp();

  it('should return UP on /health', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('UP');
    expect(res.body.service).toBe('api-gateway');
  });

  it('should list configured routes on /routes', async () => {
    const res = await request(app).get('/routes');
    expect(res.status).toBe(200);
    expect(res.body.routes.length).toBeGreaterThan(5);
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_auth_service():
    svc_dir = "services/auth-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/auth-service",
  "version": "1.0.0",
  "description": "NovaCommerce IAM, OAuth2/OIDC, Password Hashing and RBAC Authorization Service",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "jsonwebtoken": "^9.0.2",
    "argon2": "^0.40.1"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jsonwebtoken": "^9.0.6",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/auth-service/ services/auth-service/
RUN npm ci && npm run build --workspace=@novacommerce/auth-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/auth-service/dist ./services/auth-service/dist
COPY --from=builder /app/services/auth-service/package.json ./services/auth-service/package.json
EXPOSE 8001
CMD ["node", "services/auth-service/dist/server.js"]
""")

    # Repositories
    write_file(f"{svc_dir}/src/repositories/user-auth.repository.ts", """import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { UserEntity } from '@novacommerce/core-types';

export interface IUserAuthRepository {
  findById(id: string): Promise<UserEntity | null>;
  findByEmail(email: string): Promise<UserEntity | null>;
  create(user: UserEntity): Promise<UserEntity>;
  update(id: string, user: Partial<UserEntity>): Promise<UserEntity | null>;
}

export class InMemoryUserAuthRepository extends InMemoryBaseRepository<UserEntity> implements IUserAuthRepository {
  public async findByEmail(email: string): Promise<UserEntity | null> {
    const normalized = email.toLowerCase().trim();
    for (const item of this.items.values()) {
      if (item.email.toLowerCase().trim() === normalized && !item.deletedAt) {
        return JSON.parse(JSON.stringify(item));
      }
    }
    return null;
  }
}
""")

    # Domain & Services
    write_file(f"{svc_dir}/src/services/password-hasher.ts", """import { createHash, randomBytes } from 'crypto';

export class PasswordHasher {
  // Deterministic and secure fallback hashing for testing and dev
  public static async hash(password: string): Promise<string> {
    const salt = randomBytes(16).toString('hex');
    const hash = createHash('sha256').update(password + salt).digest('hex');
    return `$mockargon2$${salt}$${hash}`;
  }

  public static async verify(hash: string, plainText: string): Promise<boolean> {
    if (!hash.startsWith('$mockargon2$')) return false;
    const parts = hash.split('$');
    const salt = parts[2];
    const expectedHash = parts[3];
    const testHash = createHash('sha256').update(plainText + salt).digest('hex');
    return testHash === expectedHash;
  }
}
""")

    write_file(f"{svc_dir}/src/services/token.service.ts", """import jwt from 'jsonwebtoken';
import { UserRole } from '@novacommerce/core-types';

export interface TokenPayload {
  sub: string;
  email: string;
  role: UserRole;
  orgId?: string;
}

export class TokenService {
  private readonly secret: string;
  private readonly accessExpiration: string;
  private readonly refreshExpiration: string;

  constructor(
    secret: string = process.env.JWT_SECRET || 'super_secret_local_jwt_signing_key_min_32_characters_long',
    accessExpiration: string = '15m',
    refreshExpiration: string = '7d'
  ) {
    this.secret = secret;
    this.accessExpiration = accessExpiration;
    this.refreshExpiration = refreshExpiration;
  }

  public generateAccessToken(payload: TokenPayload): string {
    return jwt.sign(payload, this.secret, { expiresIn: this.accessExpiration as any });
  }

  public generateRefreshToken(payload: TokenPayload): string {
    return jwt.sign({ sub: payload.sub, type: 'refresh' }, this.secret, { expiresIn: this.refreshExpiration as any });
  }

  public verifyToken<T = TokenPayload>(token: string): T {
    return jwt.verify(token, this.secret) as T;
  }
}
""")

    write_file(f"{svc_dir}/src/services/auth.service.ts", """import { IUserAuthRepository } from '../repositories/user-auth.repository.js';
import { PasswordHasher } from './password-hasher.js';
import { TokenService } from './token.service.js';
import { RegisterUserDTO, LoginUserDTO, AuthTokensResponseDTO } from '@novacommerce/core-types';
import { UserRole, AccountStatus, KycStatus, ConflictError, UnauthorizedError, NotFoundError } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class AuthService {
  private readonly repo: IUserAuthRepository;
  private readonly tokenService: TokenService;
  private readonly eventBus?: IEventBus;

  constructor(repo: IUserAuthRepository, tokenService: TokenService, eventBus?: IEventBus) {
    this.repo = repo;
    this.tokenService = tokenService;
    this.eventBus = eventBus;
  }

  public async register(dto: RegisterUserDTO, correlationId?: string): Promise<AuthTokensResponseDTO> {
    const existing = await this.repo.findByEmail(dto.email);
    if (existing) {
      throw new ConflictError(`User with email '${dto.email}' already exists.`);
    }

    const passwordHash = await PasswordHasher.hash(dto.password);
    const userId = randomUUID();

    const newUser = await this.repo.create({
      id: userId,
      email: dto.email,
      passwordHash,
      role: dto.role || UserRole.CUSTOMER,
      status: AccountStatus.ACTIVE,
      kycStatus: KycStatus.NOT_SUBMITTED,
      isMfaEnabled: false,
      failedLoginAttempts: 0,
      createdAt: new Date(),
      updatedAt: new Date()
    });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.AUTH_USER_REGISTERED,
        userId,
        'User',
        {
          userId,
          email: dto.email,
          role: newUser.role,
          firstName: dto.firstName,
          lastName: dto.lastName,
          phoneNumber: dto.phoneNumber
        },
        'auth-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    const accessToken = this.tokenService.generateAccessToken({
      sub: newUser.id,
      email: newUser.email,
      role: newUser.role
    });

    const refreshToken = this.tokenService.generateRefreshToken({
      sub: newUser.id,
      email: newUser.email,
      role: newUser.role
    });

    return {
      accessToken,
      refreshToken,
      expiresInSeconds: 900,
      tokenType: 'Bearer',
      user: {
        id: newUser.id,
        email: newUser.email,
        role: newUser.role,
        firstName: dto.firstName,
        lastName: dto.lastName
      }
    };
  }

  public async login(dto: LoginUserDTO, correlationId?: string): Promise<AuthTokensResponseDTO> {
    const user = await this.repo.findByEmail(dto.email);
    if (!user) {
      throw new UnauthorizedError('Invalid email or password.');
    }

    if (user.status === AccountStatus.LOCKED || user.status === AccountStatus.SUSPENDED) {
      throw new UnauthorizedError('Account is locked or suspended.');
    }

    const isValid = await PasswordHasher.verify(user.passwordHash, dto.password);
    if (!isValid) {
      await this.repo.update(user.id, {
        failedLoginAttempts: user.failedLoginAttempts + 1
      });
      throw new UnauthorizedError('Invalid email or password.');
    }

    await this.repo.update(user.id, {
      failedLoginAttempts: 0,
      lastLoginAt: new Date()
    });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.AUTH_USER_LOGGED_IN,
        user.id,
        'User',
        { userId: user.id, email: user.email },
        'auth-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    const accessToken = this.tokenService.generateAccessToken({
      sub: user.id,
      email: user.email,
      role: user.role
    });

    const refreshToken = this.tokenService.generateRefreshToken({
      sub: user.id,
      email: user.email,
      role: user.role
    });

    return {
      accessToken,
      refreshToken,
      expiresInSeconds: 900,
      tokenType: 'Bearer',
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        firstName: '',
        lastName: ''
      }
    };
  }

  public async getUserById(id: string) {
    const user = await this.repo.findById(id);
    if (!user) {
      throw new NotFoundError('User', id);
    }
    return {
      id: user.id,
      email: user.email,
      role: user.role,
      status: user.status,
      kycStatus: user.kycStatus,
      createdAt: user.createdAt
    };
  }
}
""")

    # Controllers & Routes
    write_file(f"{svc_dir}/src/controllers/auth.controller.ts", """import { Request, Response, NextFunction } from 'express';
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
""")

    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
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
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createAuthApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('auth-service');
const port = parseInt(process.env.AUTH_SERVICE_PORT || '8001', 10);
const app = createAuthApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Auth Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Auth Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/auth.test.ts", """import request from 'supertest';
import { createAuthApp } from '../src/app.js';
import { InMemoryUserAuthRepository } from '../src/repositories/user-auth.repository.js';

describe('Auth Service Suite', () => {
  let app: any;

  beforeEach(() => {
    app = createAuthApp(new InMemoryUserAuthRepository());
  });

  it('should register a new user and return JWT tokens', async () => {
    const res = await request(app)
      .post('/api/v1/auth/register')
      .send({
        email: 'developer@novacommerce.io',
        password: 'Password123!',
        firstName: 'John',
        lastName: 'Engineer'
      });

    expect(res.status).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.data.accessToken).toBeDefined();
    expect(res.body.data.user.email).toBe('developer@novacommerce.io');
  });

  it('should login an existing registered user', async () => {
    await request(app)
      .post('/api/v1/auth/register')
      .send({
        email: 'developer@novacommerce.io',
        password: 'Password123!',
        firstName: 'John',
        lastName: 'Engineer'
      });

    const loginRes = await request(app)
      .post('/api/v1/auth/login')
      .send({
        email: 'developer@novacommerce.io',
        password: 'Password123!'
      });

    expect(loginRes.status).toBe(200);
    expect(loginRes.body.data.accessToken).toBeDefined();
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_user_service():
    svc_dir = "services/user-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/user-service",
  "version": "1.0.0",
  "description": "NovaCommerce User Profile, Organization, and Address Book Management",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/user-service/ services/user-service/
RUN npm ci && npm run build --workspace=@novacommerce/user-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/user-service/dist ./services/user-service/dist
COPY --from=builder /app/services/user-service/package.json ./services/user-service/package.json
EXPOSE 8002
CMD ["node", "services/user-service/dist/server.js"]
""")

    # Repositories
    write_file(f"{svc_dir}/src/repositories/user-profile.repository.ts", """import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { UserProfileEntity, AddressEntity } from '@novacommerce/core-types';

export class InMemoryUserProfileRepository extends InMemoryBaseRepository<UserProfileEntity> {
  public async findByUserId(userId: string): Promise<UserProfileEntity | null> {
    for (const item of this.items.values()) {
      if (item.userId === userId) return JSON.parse(JSON.stringify(item));
    }
    return null;
  }
}

export class InMemoryAddressRepository extends InMemoryBaseRepository<AddressEntity> {
  public async findByUserId(userId: string): Promise<AddressEntity[]> {
    return Array.from(this.items.values()).filter(a => a.userId === userId);
  }
}
""")

    # Services
    write_file(f"{svc_dir}/src/services/user-profile.service.ts", """import { InMemoryUserProfileRepository, InMemoryAddressRepository } from '../repositories/user-profile.repository.js';
import { UserProfileEntity, AddressEntity, NotFoundError } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class UserProfileService {
  private readonly profileRepo: InMemoryUserProfileRepository;
  private readonly addressRepo: InMemoryAddressRepository;

  constructor(profileRepo: InMemoryUserProfileRepository, addressRepo: InMemoryAddressRepository) {
    this.profileRepo = profileRepo;
    this.addressRepo = addressRepo;
  }

  public async getProfile(userId: string): Promise<UserProfileEntity> {
    let profile = await this.profileRepo.findByUserId(userId);
    if (!profile) {
      profile = await this.profileRepo.create({
        id: randomUUID(),
        userId,
        firstName: '',
        lastName: '',
        timeZone: 'UTC',
        locale: 'en-US',
        metadata: {},
        createdAt: new Date(),
        updatedAt: new Date()
      });
    }
    return profile;
  }

  public async updateProfile(userId: string, partial: Partial<UserProfileEntity>): Promise<UserProfileEntity> {
    const profile = await this.getProfile(userId);
    const updated = await this.profileRepo.update(profile.id, partial);
    return updated!;
  }

  public async addAddress(userId: string, addressData: Omit<AddressEntity, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<AddressEntity> {
    return this.addressRepo.create({
      id: randomUUID(),
      userId,
      ...addressData,
      createdAt: new Date(),
      updatedAt: new Date()
    });
  }

  public async getAddresses(userId: string): Promise<AddressEntity[]> {
    return this.addressRepo.findByUserId(userId);
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
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
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createUserApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('user-service');
const port = parseInt(process.env.USER_SERVICE_PORT || '8002', 10);
const app = createUserApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce User Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down User Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/user.test.ts", """import request from 'supertest';
import { createUserApp } from '../src/app.js';
import jwt from 'jsonwebtoken';

describe('User Service Suite', () => {
  const app = createUserApp();
  const secret = process.env.JWT_SECRET || 'super_secret_local_jwt_signing_key_min_32_characters_long';
  const token = jwt.sign({ sub: 'user-001', email: 'test@novacommerce.io', role: 'CUSTOMER' }, secret);

  it('should get and update profile for authenticated user', async () => {
    const getRes = await request(app)
      .get('/api/v1/users/profile')
      .set('Authorization', `Bearer ${token}`);

    expect(getRes.status).toBe(200);
    expect(getRes.body.data.userId).toBe('user-001');

    const putRes = await request(app)
      .put('/api/v1/users/profile')
      .set('Authorization', `Bearer ${token}`)
      .send({ firstName: 'Alexander', lastName: 'Hamilton' });

    expect(putRes.status).toBe(200);
    expect(putRes.body.data.firstName).toBe('Alexander');
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_catalog_service():
    svc_dir = "services/catalog-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/catalog-service",
  "version": "1.0.0",
  "description": "NovaCommerce Product Catalog, SKU, Category, and Pricing Management",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/catalog-service/ services/catalog-service/
RUN npm ci && npm run build --workspace=@novacommerce/catalog-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/catalog-service/dist ./services/catalog-service/dist
COPY --from=builder /app/services/catalog-service/package.json ./services/catalog-service/package.json
EXPOSE 8003
CMD ["node", "services/catalog-service/dist/server.js"]
""")

    # Repositories
    write_file(f"{svc_dir}/src/repositories/product.repository.ts", """import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { ProductEntity, CategoryEntity } from '@novacommerce/core-types';

export class InMemoryProductRepository extends InMemoryBaseRepository<ProductEntity> {
  public async findBySku(sku: string): Promise<ProductEntity | null> {
    for (const p of this.items.values()) {
      if (p.sku === sku && !p.deletedAt) return JSON.parse(JSON.stringify(p));
    }
    return null;
  }
}

export class InMemoryCategoryRepository extends InMemoryBaseRepository<CategoryEntity> {}
""")

    # Service
    write_file(f"{svc_dir}/src/services/catalog.service.ts", """import { InMemoryProductRepository, InMemoryCategoryRepository } from '../repositories/product.repository.js';
import { ProductEntity, CategoryEntity, CreateProductDTO, NotFoundError, ConflictError } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class CatalogService {
  private readonly productRepo: InMemoryProductRepository;
  private readonly categoryRepo: InMemoryCategoryRepository;
  private readonly eventBus?: IEventBus;

  constructor(productRepo: InMemoryProductRepository, categoryRepo: InMemoryCategoryRepository, eventBus?: IEventBus) {
    this.productRepo = productRepo;
    this.categoryRepo = categoryRepo;
    this.eventBus = eventBus;
  }

  public async createProduct(dto: CreateProductDTO, correlationId?: string): Promise<ProductEntity> {
    const existing = await this.productRepo.findBySku(dto.sku);
    if (existing) {
      throw new ConflictError(`Product with SKU '${dto.sku}' already exists.`);
    }

    const product: ProductEntity = {
      id: randomUUID(),
      sku: dto.sku,
      name: dto.name,
      slug: dto.slug,
      description: dto.description,
      categoryId: dto.categoryId,
      basePrice: dto.basePrice,
      isActive: dto.isActive,
      tags: dto.tags,
      attributes: dto.attributes,
      images: [],
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const saved = await this.productRepo.create(product);

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.CATALOG_PRODUCT_CREATED,
        saved.id,
        'Product',
        saved,
        'catalog-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return saved;
  }

  public async getProductById(id: string): Promise<ProductEntity> {
    const product = await this.productRepo.findById(id);
    if (!product || product.deletedAt) {
      throw new NotFoundError('Product', id);
    }
    return product;
  }

  public async listProducts(limit: number = 20, offset: number = 0): Promise<{ items: ProductEntity[]; total: number }> {
    const items = await this.productRepo.findAll({ isActive: true } as any, limit, offset);
    const total = await this.productRepo.count({ isActive: true } as any);
    return { items, total };
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, RequestValidator } from '@novacommerce/core-middleware';
import { InMemoryProductRepository, InMemoryCategoryRepository } from './repositories/product.repository.js';
import { CatalogService } from './services/catalog.service.js';
import { CreateProductSchema } from '@novacommerce/core-types';

export function createCatalogApp(): Express {
  const app = express();
  const logger = Logger.create('catalog-service');
  const service = new CatalogService(new InMemoryProductRepository(), new InMemoryCategoryRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'catalog-service' }));

  app.get('/api/v1/catalog/products', async (req, res, next) => {
    try {
      const page = parseInt(req.query.page as string || '1', 10);
      const limit = parseInt(req.query.limit as string || '20', 10);
      const offset = (page - 1) * limit;
      const result = await service.listProducts(limit, offset);
      res.json({
        success: true,
        data: result.items,
        meta: { page, limit, totalItems: result.total }
      });
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/v1/catalog/products/:id', async (req, res, next) => {
    try {
      const product = await service.getProductById(req.params.id);
      res.json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  });

  app.post('/api/v1/catalog/products', RequestValidator.validateBody(CreateProductSchema), async (req, res, next) => {
    try {
      const product = await service.createProduct(req.body);
      res.status(201).json({ success: true, data: product });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createCatalogApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('catalog-service');
const port = parseInt(process.env.CATALOG_SERVICE_PORT || '8003', 10);
const app = createCatalogApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Catalog Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Catalog Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/catalog.test.ts", """import request from 'supertest';
import { createCatalogApp } from '../src/app.js';
import { Currency } from '@novacommerce/core-types';

describe('Catalog Service Suite', () => {
  const app = createCatalogApp();

  it('should create and fetch product', async () => {
    const createRes = await request(app)
      .post('/api/v1/catalog/products')
      .send({
        sku: 'SKU-LAPTOP-01',
        name: 'Pro Ultrabook 16-inch',
        slug: 'pro-ultrabook-16',
        description: 'High performance engineer laptop',
        categoryId: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
        basePrice: { amount: 199900, currency: Currency.USD },
        tags: ['electronics', 'computers']
      });

    expect(createRes.status).toBe(201);
    const productId = createRes.body.data.id;

    const getRes = await request(app).get(`/api/v1/catalog/products/${productId}`);
    expect(getRes.status).toBe(200);
    expect(getRes.body.data.sku).toBe('SKU-LAPTOP-01');
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_inventory_service():
    svc_dir = "services/inventory-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/inventory-service",
  "version": "1.0.0",
  "description": "NovaCommerce Inventory Stock Reservation and Warehouse Management",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/inventory-service/ services/inventory-service/
RUN npm ci && npm run build --workspace=@novacommerce/inventory-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/inventory-service/dist ./services/inventory-service/dist
COPY --from=builder /app/services/inventory-service/package.json ./services/inventory-service/package.json
EXPOSE 8009
CMD ["node", "services/inventory-service/dist/server.js"]
""")

    # Repositories & Service
    write_file(f"{svc_dir}/src/repositories/inventory.repository.ts", """import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { InventoryStockEntity, InventoryReservationEntity } from '@novacommerce/core-types';

export class InMemoryStockRepository extends InMemoryBaseRepository<InventoryStockEntity> {
  public async findBySku(sku: string): Promise<InventoryStockEntity | null> {
    for (const item of this.items.values()) {
      if (item.sku === sku) return JSON.parse(JSON.stringify(item));
    }
    return null;
  }
}

export class InMemoryReservationRepository extends InMemoryBaseRepository<InventoryReservationEntity> {
  public async findByOrderId(orderId: string): Promise<InventoryReservationEntity[]> {
    return Array.from(this.items.values()).filter(r => r.orderId === orderId);
  }
}
""")

    write_file(f"{svc_dir}/src/services/inventory.service.ts", """import { InMemoryStockRepository, InMemoryReservationRepository } from '../repositories/inventory.repository.js';
import { InventoryStockEntity, InventoryReservationEntity, InsufficientStockError, NotFoundError } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class InventoryService {
  private readonly stockRepo: InMemoryStockRepository;
  private readonly reservationRepo: InMemoryReservationRepository;
  private readonly eventBus?: IEventBus;

  constructor(stockRepo: InMemoryStockRepository, reservationRepo: InMemoryReservationRepository, eventBus?: IEventBus) {
    this.stockRepo = stockRepo;
    this.reservationRepo = reservationRepo;
    this.eventBus = eventBus;
  }

  public async setStock(sku: string, warehouseId: string, quantity: number): Promise<InventoryStockEntity> {
    let stock = await this.stockRepo.findBySku(sku);
    if (!stock) {
      stock = await this.stockRepo.create({
        id: randomUUID(),
        sku,
        warehouseId,
        onHandQuantity: quantity,
        reservedQuantity: 0,
        allocatedQuantity: 0,
        safetyStockThreshold: 5,
        reorderQuantity: 20,
        version: 1,
        updatedAt: new Date()
      });
    } else {
      stock = await this.stockRepo.update(stock.id, {
        onHandQuantity: quantity,
        version: stock.version + 1
      }) as InventoryStockEntity;
    }
    return stock;
  }

  public async reserveStock(orderId: string, sku: string, quantity: number, correlationId?: string): Promise<InventoryReservationEntity> {
    const stock = await this.stockRepo.findBySku(sku);
    if (!stock) {
      throw new NotFoundError('InventoryStock for SKU', sku);
    }

    const available = stock.onHandQuantity - stock.reservedQuantity;
    if (available < quantity) {
      throw new InsufficientStockError(sku, quantity, available);
    }

    await this.stockRepo.update(stock.id, {
      reservedQuantity: stock.reservedQuantity + quantity,
      version: stock.version + 1
    });

    const reservation = await this.reservationRepo.create({
      id: randomUUID(),
      reservationCode: `RES-${randomUUID().substring(0, 8).toUpperCase()}`,
      orderId,
      sku,
      warehouseId: stock.warehouseId,
      quantity,
      isCommitted: false,
      isReleased: false,
      expiresAt: new Date(Date.now() + 30 * 60 * 1000), // 30 mins
      createdAt: new Date(),
      updatedAt: new Date()
    });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.INVENTORY_RESERVATION_CREATED,
        reservation.id,
        'InventoryReservation',
        reservation,
        'inventory-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return reservation;
  }

  public async releaseReservation(orderId: string, correlationId?: string): Promise<void> {
    const reservations = await this.reservationRepo.findByOrderId(orderId);
    for (const res of reservations) {
      if (!res.isReleased && !res.isCommitted) {
        const stock = await this.stockRepo.findBySku(res.sku);
        if (stock) {
          await this.stockRepo.update(stock.id, {
            reservedQuantity: Math.max(0, stock.reservedQuantity - res.quantity),
            version: stock.version + 1
          });
        }
        await this.reservationRepo.update(res.id, { isReleased: true });

        if (this.eventBus) {
          const event = DomainEventFactory.create(
            EventType.INVENTORY_RESERVATION_RELEASED,
            res.id,
            'InventoryReservation',
            res,
            'inventory-service',
            correlationId
          );
          await this.eventBus.publish(event);
        }
      }
    }
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { InMemoryStockRepository, InMemoryReservationRepository } from './repositories/inventory.repository.js';
import { InventoryService } from './services/inventory.service.js';

export function createInventoryApp(): Express {
  const app = express();
  const logger = Logger.create('inventory-service');
  const service = new InventoryService(new InMemoryStockRepository(), new InMemoryReservationRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'inventory-service' }));

  app.post('/api/v1/inventory/stock', async (req, res, next) => {
    try {
      const { sku, warehouseId, quantity } = req.body;
      const stock = await service.setStock(sku, warehouseId || 'WH-MAIN-01', quantity);
      res.json({ success: true, data: stock });
    } catch (err) {
      next(err);
    }
  });

  app.post('/api/v1/inventory/reserve', async (req, res, next) => {
    try {
      const { orderId, sku, quantity } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const reservation = await service.reserveStock(orderId, sku, quantity, correlationId);
      res.status(201).json({ success: true, data: reservation });
    } catch (err) {
      next(err);
    }
  });

  app.post('/api/v1/inventory/release', async (req, res, next) => {
    try {
      const { orderId } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      await service.releaseReservation(orderId, correlationId);
      res.json({ success: true, message: `Reservations for order ${orderId} released.` });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createInventoryApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('inventory-service');
const port = parseInt(process.env.INVENTORY_SERVICE_PORT || '8009', 10);
const app = createInventoryApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Inventory Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Inventory Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/inventory.test.ts", """import request from 'supertest';
import { createInventoryApp } from '../src/app.js';

describe('Inventory Service Suite', () => {
  const app = createInventoryApp();

  it('should set stock and reserve successfully', async () => {
    await request(app)
      .post('/api/v1/inventory/stock')
      .send({ sku: 'SKU-PHONE-128', quantity: 50 });

    const res = await request(app)
      .post('/api/v1/inventory/reserve')
      .send({ orderId: 'ord-test-001', sku: 'SKU-PHONE-128', quantity: 2 });

    expect(res.status).toBe(201);
    expect(res.body.data.quantity).toBe(2);
  });

  it('should fail reservation if insufficient stock', async () => {
    const res = await request(app)
      .post('/api/v1/inventory/reserve')
      .send({ orderId: 'ord-test-002', sku: 'SKU-PHONE-128', quantity: 9999 });

    expect(res.status).toBe(400);
    expect(res.body.error.code).toBe('ERR_INVENTORY_INSUFFICIENT_STOCK');
  });
});
""")
    print(f"Generated {svc_dir}")

if __name__ == "__main__":
    generate_api_gateway()
    generate_auth_service()
    generate_user_service()
    generate_catalog_service()
    generate_inventory_service()
    print("Services Part 1 generated successfully.")
