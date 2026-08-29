import { Logger } from '@novacommerce/core-logger';

export interface SagaTransactionContextV5 {
  sagaId: string;
  orderId: string;
  currentStepIndex: number;
  totalSteps: number;
  isCompensating: boolean;
  compensationLog: string[];
}

export class UserServiceSagaStepCoordinatorV5 {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async executeForwardStep(ctx: SagaTransactionContextV5, stepName: string, action: () => Promise<boolean>): Promise<boolean> {
    this.logger.info(`Executing forward saga step [${stepName}] for saga ${ctx.sagaId} in user-service`);
    try {
      const success = await action();
      if (success) {
        ctx.compensationLog.push(stepName);
        ctx.currentStepIndex++;
      }
      return success;
    } catch (err) {
      this.logger.error(`Forward step [${stepName}] failed in user-service:`, err);
      return false;
    }
  }

  public async executeCompensation(ctx: SagaTransactionContextV5, compensatorMap: Record<string, () => Promise<void>>): Promise<void> {
    this.logger.warn(`Triggering saga rollback compensation for saga ${ctx.sagaId} in user-service`);
    ctx.isCompensating = true;

    // Rollback in reverse order
    const reverseSteps = [...ctx.compensationLog].reverse();
    for (const step of reverseSteps) {
      const compFn = compensatorMap[step];
      if (compFn) {
        this.logger.info(`Compensating step [${step}] in user-service`);
        try {
          await compFn();
        } catch (err) {
          this.logger.error(`Failed to compensate step [${step}] in user-service:`, err);
        }
      }
    }
  }
}
