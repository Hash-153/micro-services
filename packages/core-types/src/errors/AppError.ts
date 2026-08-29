import { ErrorCode } from '../enums/ErrorCode.js';

export class AppError extends Error {
  public readonly statusCode: number;
  public readonly code: ErrorCode;
  public readonly isOperational: boolean;
  public readonly details?: Record<string, unknown> | unknown[];

  constructor(
    message: string,
    statusCode: number = 500,
    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
    details?: Record<string, unknown> | unknown[],
    isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: Record<string, unknown> | unknown[]) {
    super(message, 400, ErrorCode.VALIDATION_ERROR, details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, identifier?: string) {
    const message = identifier ? `${resource} with id '${identifier}' was not found.` : `${resource} was not found.`;
    super(message, 404, ErrorCode.NOT_FOUND, { resource, identifier });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Authentication credentials are invalid or missing.') {
    super(message, 401, ErrorCode.UNAUTHORIZED);
  }
}

export class ForbiddenError extends AppError {
  constructor(message: string = 'You do not possess sufficient permissions to perform this operation.') {
    super(message, 403, ErrorCode.FORBIDDEN);
  }
}

export class ConflictError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 409, ErrorCode.CONFLICT, details);
  }
}

export class InsufficientStockError extends AppError {
  constructor(sku: string, requested: number, available: number) {
    super(`Insufficient stock for SKU '${sku}'. Requested: ${requested}, Available: ${available}`, 400, ErrorCode.INSUFFICIENT_STOCK, {
      sku,
      requested,
      available
    });
  }
}

export class SagaExecutionError extends AppError {
  constructor(sagaName: string, stepFailed: string, originalError: Error) {
    super(`Saga '${sagaName}' failed at step '${stepFailed}': ${originalError.message}`, 500, ErrorCode.SAGA_EXECUTION_FAILED, {
      sagaName,
      stepFailed,
      originalMessage: originalError.message
    });
  }
}
