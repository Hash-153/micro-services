import { ZodSchema, ZodError } from 'zod';
import { ValidationError } from '@novacommerce/core-types';

export class RequestValidator {
  public static validateBody<T>(schema: ZodSchema<T>) {
    return (req: any, res: any, next: any) => {
      try {
        req.body = schema.parse(req.body);
        return next();
      } catch (err) {
        if (err instanceof ZodError) {
          const formatted = err.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message
          }));
          return next(new ValidationError('Invalid request payload', formatted));
        }
        return next(err);
      }
    };
  }

  public static validateQuery<T>(schema: ZodSchema<T>) {
    return (req: any, res: any, next: any) => {
      try {
        req.query = schema.parse(req.query);
        return next();
      } catch (err) {
        if (err instanceof ZodError) {
          const formatted = err.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message
          }));
          return next(new ValidationError('Invalid query parameters', formatted));
        }
        return next(err);
      }
    };
  }
}
