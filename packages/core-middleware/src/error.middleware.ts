import { AppError, ApiErrorResponse, ErrorCode } from '@novacommerce/core-types';
import { ILogger } from '@novacommerce/core-logger';

export class ErrorHandlerMiddleware {
  public static handle(logger: ILogger) {
    return (err: any, req: any, res: any, next: any) => {
      const correlationId = req.headers['x-correlation-id'] || 'no-correlation-id';
      
      let statusCode = 500;
      let errorCode = ErrorCode.INTERNAL_SERVER_ERROR;
      let message = 'An internal server error occurred.';
      let details: any = undefined;

      if (err instanceof AppError) {
        statusCode = err.statusCode;
        errorCode = err.code;
        message = err.message;
        details = err.details;
      } else if (err.status || err.statusCode) {
        statusCode = err.status || err.statusCode;
        message = err.message || message;
      }

      logger.error(`HTTP Request failed: ${req.method} ${req.originalUrl || req.url}`, err, {
        correlationId,
        statusCode,
        errorCode
      });

      const responsePayload: ApiErrorResponse = {
        success: false,
        statusCode,
        error: {
          code: errorCode,
          message,
          details,
          correlationId: typeof correlationId === 'string' ? correlationId : correlationId[0],
          timestamp: new Date().toISOString()
        }
      };

      res.status(statusCode).json(responsePayload);
    };
  }
}
