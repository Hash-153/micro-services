import jwt from 'jsonwebtoken';
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
