import { NotificationChannel } from '@novacommerce/core-types';

export interface UserNotificationPreferences {
  userId: string;
  orderUpdatesChannel: NotificationChannel;
  promotionsChannel: NotificationChannel;
  securityAlertsChannel: NotificationChannel;
  doNotDisturb: boolean;
  quietHoursStartLocal?: string; // "22:00"
  quietHoursEndLocal?: string;   // "07:00"
}

export class NotificationDeliveryRouter {
  public static selectChannel(
    notificationType: 'ORDER_UPDATE' | 'PROMOTION' | 'SECURITY_ALERT',
    prefs: UserNotificationPreferences
  ): { channel: NotificationChannel; shouldSuppress: boolean; reason?: string } {
    if (prefs.doNotDisturb && notificationType !== 'SECURITY_ALERT') {
      return { channel: NotificationChannel.IN_APP, shouldSuppress: true, reason: 'User is in Do Not Disturb mode' };
    }

    switch (notificationType) {
      case 'SECURITY_ALERT':
        // Security alerts always deliver immediately via SMS or Email
        return { channel: prefs.securityAlertsChannel || NotificationChannel.EMAIL, shouldSuppress: false };
      case 'ORDER_UPDATE':
        return { channel: prefs.orderUpdatesChannel || NotificationChannel.EMAIL, shouldSuppress: false };
      case 'PROMOTION':
        return { channel: prefs.promotionsChannel || NotificationChannel.EMAIL, shouldSuppress: false };
    }
  }
}
