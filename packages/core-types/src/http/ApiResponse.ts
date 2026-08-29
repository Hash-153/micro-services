export interface ApiResponse<T = unknown> {
  success: boolean;
  statusCode: number;
  data: T;
  meta?: ResponseMetadata;
}

export interface ApiErrorResponse {
  success: false;
  statusCode: number;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown> | unknown[];
    correlationId?: string;
    timestamp: string;
  };
}

export interface ResponseMetadata {
  page?: number;
  limit?: number;
  totalItems?: number;
  totalPages?: number;
  hasNextPage?: boolean;
  hasPrevPage?: boolean;
  correlationId?: string;
  executionTimeMs?: number;
}
