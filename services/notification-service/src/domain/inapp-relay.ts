import { Logger } from '@novacommerce/core-logger';

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
