import { Logger } from '@novacommerce/core-logger';

export interface WebSocketClientConnection {
  socketId: string;
  userId?: string;
  subscriptions: Set<string>;
  connectedAt: Date;
}

export class GatewayWebSocketHub {
  private logger: Logger;
  private clients: Map<string, WebSocketClientConnection> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public registerClient(socketId: string, userId?: string): void {
    this.clients.set(socketId, {
      socketId,
      userId,
      subscriptions: new Set(),
      connectedAt: new Date()
    });
    this.logger.info(`WebSocket client connected: ${socketId} (user: ${userId || 'anonymous'})`);
  }

  public removeClient(socketId: string): void {
    this.clients.delete(socketId);
    this.logger.info(`WebSocket client disconnected: ${socketId}`);
  }

  public subscribeToTopic(socketId: string, topic: string): void {
    const client = this.clients.get(socketId);
    if (client) {
      client.subscriptions.add(topic);
    }
  }

  public broadcastToTopic(topic: string, messagePayload: any): number {
    let sentCount = 0;
    for (const client of this.clients.values()) {
      if (client.subscriptions.has(topic)) {
        // In production transmits WebSocket frame
        sentCount++;
      }
    }
    return sentCount;
  }
}
