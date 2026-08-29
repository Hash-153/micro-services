export interface QueueBindingDefinition {
  queueName: string;
  exchangeName: string;
  routingKeyPattern: string;
  deadLetterExchange?: string;
  deadLetterRoutingKey?: string;
  messageTtlMs?: number;
  maxPriority?: number;
}

export class RabbitMqTopologyManager {
  private static readonly MAIN_EXCHANGE = 'novacommerce.events';
  private static readonly DLX_EXCHANGE = 'novacommerce.dlx';
  private static readonly DLQ_QUEUE = 'novacommerce.dlq';

  public static getStandardBindings(): QueueBindingDefinition[] {
    return [
      {
        queueName: 'q.auth.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'auth.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.auth'
      },
      {
        queueName: 'q.user.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'user.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.user'
      },
      {
        queueName: 'q.catalog.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'catalog.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.catalog'
      },
      {
        queueName: 'q.inventory.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'inventory.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.inventory'
      },
      {
        queueName: 'q.order.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'order.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.order'
      },
      {
        queueName: 'q.payment.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'payment.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.payment'
      },
      {
        queueName: 'q.fulfillment.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'fulfillment.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.fulfillment'
      },
      {
        queueName: 'q.notification.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'notification.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.notification'
      },
      {
        queueName: 'q.analytics.events',
        exchangeName: this.MAIN_EXCHANGE,
        routingKeyPattern: 'analytics.#',
        deadLetterExchange: this.DLX_EXCHANGE,
        deadLetterRoutingKey: 'dlq.analytics'
      }
    ];
  }
}
