import { Logger } from '@novacommerce/core-logger';

export interface GrpcServiceDefinition {
  serviceName: string;
  methods: Record<string, (call: any) => Promise<any>>;
}

export class MockGrpcServer {
  private logger: Logger;
  private port: number;
  private services: Map<string, GrpcServiceDefinition> = new Map();
  private isRunning: boolean = false;

  constructor(port: number, logger: Logger) {
    this.port = port;
    this.logger = logger;
  }

  public registerService(service: GrpcServiceDefinition): void {
    this.services.set(service.serviceName, service);
    this.logger.info(`Registered gRPC service: ${service.serviceName}`);
  }

  public async start(): Promise<void> {
    this.isRunning = true;
    this.logger.info(`Mock gRPC Server listening on port ${this.port}`);
  }

  public async stop(): Promise<void> {
    this.isRunning = false;
    this.logger.info(`Mock gRPC Server on port ${this.port} stopped.`);
  }

  public async invokeMethod(serviceName: string, methodName: string, requestPayload: any): Promise<any> {
    if (!this.isRunning) {
      throw new Error(`gRPC Server on port ${this.port} is not running.`);
    }

    const service = this.services.get(serviceName);
    if (!service) {
      throw new Error(`gRPC Service '${serviceName}' not found.`);
    }

    const handler = service.methods[methodName];
    if (!handler) {
      throw new Error(`gRPC Method '${methodName}' not found on service '${serviceName}'.`);
    }

    return await handler({ request: requestPayload });
  }
}
