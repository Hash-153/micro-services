import { IUserAuthRepository } from '../repositories/user-auth.repository.js';
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
