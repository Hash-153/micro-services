import { UserRole, UnauthorizedError, ForbiddenError } from '@novacommerce/core-types';
import jwt from 'jsonwebtoken';

export interface AuthenticatedUser {
  id: string;
  email: string;
  role: UserRole;
  organizationId?: string;
}

export interface RequestWithUser {
  user?: AuthenticatedUser;
  headers: Record<string, string | string[] | undefined>;
}

export class AuthMiddleware {
  public static verifyToken(secret: string) {
    return (req: any, res: any, next: any) => {
      const authHeader = req.headers['authorization'] || req.headers['Authorization'];
      if (!authHeader || typeof authHeader !== 'string') {
        return next(new UnauthorizedError('Missing Authorization header'));
      }

      const parts = authHeader.split(' ');
      if (parts.length !== 2 || parts[0] !== 'Bearer') {
        return next(new UnauthorizedError('Invalid Authorization header format. Expected Bearer token.'));
      }

      const token = parts[1]!;
      try {
        const decoded = jwt.verify(token, secret) as AuthenticatedUser;
        req.user = decoded;
        return next();
      } catch (err: any) {
        return next(new UnauthorizedError(`Invalid token: ${err.message}`));
      }
    };
  }

  public static requireRoles(...allowedRoles: UserRole[]) {
    return (req: any, res: any, next: any) => {
      if (!req.user) {
        return next(new UnauthorizedError('User is not authenticated.'));
      }

      if (!allowedRoles.includes(req.user.role)) {
        return next(new ForbiddenError(`Role ${req.user.role} does not have permission to access this resource.`));
      }

      return next();
    };
  }
}
