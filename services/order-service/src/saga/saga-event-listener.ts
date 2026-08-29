import { IEventBus, IDomainEvent } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';
import { OrderService } from '../services/order.service.js';

export class SagaEventListener {
  private eventBus: IEventBus;
  private logger: Logger;
  private orderService: OrderService;

  constructor(eventBus: IEventBus, logger: Logger, orderService: OrderService) {
    this.eventBus = eventBus;
    this.logger = logger;
    this.orderService = orderService;
  }

  public async startListening(): Promise<void> {
    await this.eventBus.subscribe('payment.captured', this.handlePaymentCaptured);
    await this.eventBus.subscribe('payment.failed', this.handlePaymentFailed);
    await this.eventBus.subscribe('fulfillment.shipment.delivered', this.handleShipmentDelivered);
    this.logger.info('Saga Event Listener successfully subscribed to domain event topics.');
  }

  private handlePaymentCaptured = async (event: IDomainEvent<{ orderId: string; transactionReference: string }>) => {
    this.logger.info(`Saga listener received payment.captured for order ${event.payload.orderId}`);
  };

  private handlePaymentFailed = async (event: IDomainEvent<{ orderId: string; failureReason: string }>) => {
    this.logger.warn(`Saga listener received payment.failed for order ${event.payload.orderId}: ${event.payload.failureReason}`);
  };

  private handleShipmentDelivered = async (event: IDomainEvent<{ orderId: string; shipmentNumber: string }>) => {
    this.logger.info(`Saga listener received fulfillment.shipment.delivered for order ${event.payload.orderId}`);
  };
}
