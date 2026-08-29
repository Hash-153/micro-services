export interface GrpcServiceConfig {
  host: string;
  port: number;
  timeoutMs?: number;
  maxRetries?: number;
}

export interface GrpcMetadata {
  correlationId?: string;
  userId?: string;
  authorization?: string;
}

export interface IGrpcClientPool<T> {
  getClient(): Promise<T>;
  releaseClient(client: T): void;
}
