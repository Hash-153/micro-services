import { Logger } from '@novacommerce/core-logger';

export interface DomainOperationContextV5 {
  traceId: string;
  userId: string;
  tenantId: string;
  operationName: string;
  initiatedAt: Date;
}

export interface OperationResultV5<T> {
  isSuccess: boolean;
  data?: T;
  errorCode?: string;
  errorMessage?: string;
  auditRecordId: string;
}

export class CatalogServiceDomainServiceV5 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async executePipeline<TInput, TOutput>(
    ctx: DomainOperationContextV5,
    input: TInput,
    processor: (ctx: DomainOperationContextV5, input: TInput) => Promise<TOutput>
  ): Promise<OperationResultV5<TOutput>> {
    this.logger.info(`Starting enterprise pipeline [${ctx.operationName}] for tenant ${ctx.tenantId} (trace: ${ctx.traceId}) in catalog-service`);

    try {
      this.validateContext(ctx);
      const output = await processor(ctx, input);

      const auditId = `aud_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
      this.logger.info(`Pipeline [${ctx.operationName}] completed successfully. AuditId: ${auditId}`);

      return {
        isSuccess: true,
        data: output,
        auditRecordId: auditId
      };
    } catch (err: any) {
      this.logger.error(`Pipeline [${ctx.operationName}] failed in catalog-service:`, err);
      return {
        isSuccess: false,
        errorCode: 'ERR_DOMAIN_EXECUTION_FAILURE',
        errorMessage: err.message,
        auditRecordId: `aud_err_${Date.now()}`
      };
    }
  }

  private validateContext(ctx: DomainOperationContextV5): void {
    if (!ctx.traceId || !ctx.tenantId || !ctx.operationName) {
      throw new Error('Invalid DomainOperationContext: traceId, tenantId, and operationName are required');
    }
  }
}
