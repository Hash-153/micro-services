import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_quantum():
    print("Generating comprehensive Production Quantum Modules...")

    # 1. API Gateway WebSocket Real-Time Gateway Hub
    write_file("services/api-gateway/src/websocket/gateway-ws-hub.ts", """import { Logger } from '@novacommerce/core-logger';

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
""")

    # 2. Notification In-App WebSocket Relay
    write_file("services/notification-service/src/domain/inapp-relay.ts", """import { Logger } from '@novacommerce/core-logger';

export interface InAppNotification {
  id: string;
  userId: string;
  title: string;
  body: string;
  actionUrl?: string;
  isRead: boolean;
  createdAt: Date;
}

export class InAppNotificationRelay {
  private logger: Logger;
  private store: Map<string, InAppNotification[]> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async pushNotification(userId: string, title: string, body: string, actionUrl?: string): Promise<InAppNotification> {
    const notif: InAppNotification = {
      id: crypto.randomUUID(),
      userId,
      title,
      body,
      actionUrl,
      isRead: false,
      createdAt: new Date()
    };

    if (!this.store.has(userId)) {
      this.store.set(userId, []);
    }
    this.store.get(userId)!.unshift(notif);

    this.logger.info(`In-app notification created for user ${userId}: "${title}"`);
    return notif;
  }

  public async getUserNotifications(userId: string, unreadOnly: boolean = false): Promise<InAppNotification[]> {
    const list = this.store.get(userId) || [];
    return unreadOnly ? list.filter(n => !n.isRead) : list;
  }

  public async markAsRead(userId: string, notificationId: string): Promise<boolean> {
    const list = this.store.get(userId) || [];
    const notif = list.find(n => n.id === notificationId);
    if (notif) {
      notif.isRead = true;
      return true;
    }
    return false;
  }
}
""")

    print("Production quantum modules generated.")

if __name__ == "__main__":
    generate_prod_quantum()
