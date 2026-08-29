import { ISagaStep, SagaContext } from './saga-step.interface.js';
import { ILogger } from '@novacommerce/core-logger';
import { SagaExecutionError } from '@novacommerce/core-types';

export class CheckoutSagaOrchestrator {
  private readonly steps: ISagaStep[] = [];
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'CheckoutSagaOrchestrator' });
  }

  public addStep(step: ISagaStep): this {
    this.steps.push(step);
    return this;
  }

  public async execute(context: SagaContext): Promise<boolean> {
    const executedSteps: ISagaStep[] = [];
    this.logger.info(`Starting Checkout Saga for order ${context.orderId}`, { correlationId: context.correlationId });

    for (const step of this.steps) {
      try {
        this.logger.debug(`Executing saga step: ${step.name}`);
        await step.execute(context);
        executedSteps.push(step);
      } catch (err: any) {
        this.logger.error(`Saga step '${step.name}' failed. Initiating rollback compensation...`, err);
        await this.rollback(executedSteps, context);
        throw new SagaExecutionError('CheckoutSaga', step.name, err);
      }
    }

    this.logger.info(`Checkout Saga completed successfully for order ${context.orderId}`);
    return true;
  }

  private async rollback(executedSteps: ISagaStep[], context: SagaContext): Promise<void> {
    const reversed = [...executedSteps].reverse();
    for (const step of reversed) {
      try {
        this.logger.warn(`Compensating saga step: ${step.name}`);
        await step.compensate(context);
      } catch (compErr) {
        this.logger.fatal(`CRITICAL: Compensation failed for step '${step.name}'`, compErr);
      }
    }
  }
}
