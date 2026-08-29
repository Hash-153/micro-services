import { Logger } from '@novacommerce/core-logger';

export interface SagaTransactionContextV6 {
  sagaId: string;
  orderId: string;
  currentStepIndex: number;
  totalSteps: number;
  isCompensating: boolean;
  compensationLog: string[];
}

export class OrderServiceSagaStepCoordinatorV6 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async executeForwardStep(ctx: SagaTransactionContextV6, stepName: string, action: () => Promise<boolean>): Promise<boolean> {
    this.logger.info(`Executing forward saga step [${stepName}] for saga ${ctx.sagaId} in order-service`);
    try {
      const success = await action();
      if (success) {
        ctx.compensationLog.push(stepName);
        ctx.currentStepIndex++;
      }
      return success;
    } catch (err) {
      this.logger.error(`Forward step [${stepName}] failed in order-service:`, err);
      return false;
    }
  }

  public async executeCompensation(ctx: SagaTransactionContextV6, compensatorMap: Record<string, () => Promise<void>>): Promise<void> {
    this.logger.warn(`Triggering saga rollback compensation for saga ${ctx.sagaId} in order-service`);
    ctx.isCompensating = true;

    // Rollback in reverse order
    const reverseSteps = [...ctx.compensationLog].reverse();
    for (const step of reverseSteps) {
      const compFn = compensatorMap[step];
      if (compFn) {
        this.logger.info(`Compensating step [${step}] in order-service`);
        try {
          await compFn();
        } catch (err) {
          this.logger.error(`Failed to compensate step [${step}] in order-service:`, err);
        }
      }
    }
  }
}
