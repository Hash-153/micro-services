import { GrpcServiceConfig, IGrpcClientPool } from './types.js';
import { ILogger } from '@novacommerce/core-logger';

export class MockGrpcClientPool<T> implements IGrpcClientPool<T> {
  private readonly config: GrpcServiceConfig;
  private readonly clientFactory: (config: GrpcServiceConfig) => T;
  private readonly logger?: ILogger;
  private clientInstance: T | null = null;

  constructor(config: GrpcServiceConfig, clientFactory: (config: GrpcServiceConfig) => T, logger?: ILogger) {
    this.config = config;
    this.clientFactory = clientFactory;
    this.logger = logger;
  }

  public async getClient(): Promise<T> {
    if (!this.clientInstance) {
      this.clientInstance = this.clientFactory(this.config);
      this.logger?.debug(`Instantiated gRPC client connection to ${this.config.host}:${this.config.port}`);
    }
    return this.clientInstance;
  }

  public releaseClient(client: T): void {
    // Connection reuse in pool
  }
}
