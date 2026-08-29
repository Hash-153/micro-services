import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v6():
    print("Generating comprehensive Production V6 Modules...")

    # 1. Payment Multi-Currency Dynamic FX Converter
    write_file("services/payment-service/src/domain/dynamic-fx-converter.ts", """import { Currency } from '@novacommerce/core-types';

export interface FxRatePair {
  baseCurrency: Currency;
  targetCurrency: Currency;
  rate: number;
  spreadBasisPoints: number;
  lastUpdatedAt: Date;
}

export class DynamicFxConverter {
  private static readonly BASE_RATES: Map<string, FxRatePair> = new Map();

  static {
    const pairs: [Currency, Currency, number][] = [
      [Currency.USD, Currency.EUR, 0.92],
      [Currency.USD, Currency.GBP, 0.79],
      [Currency.USD, Currency.CAD, 1.36],
      [Currency.USD, Currency.AUD, 1.52],
      [Currency.USD, Currency.JPY, 155.40],
      [Currency.USD, Currency.CHF, 0.90],
      [Currency.USD, Currency.SGD, 1.35],
      [Currency.USD, Currency.INR, 83.45],
      [Currency.EUR, Currency.USD, 1.087],
      [Currency.GBP, Currency.USD, 1.265]
    ];

    for (const [base, target, rate] of pairs) {
      const key = `${base}:${target}`;
      this.BASE_RATES.set(key, {
        baseCurrency: base,
        targetCurrency: target,
        rate,
        spreadBasisPoints: 25, // 0.25% margin
        lastUpdatedAt: new Date()
      });
    }
  }

  public static convert(
    amountCents: number,
    fromCurrency: Currency,
    toCurrency: Currency
  ): { convertedAmountCents: number; effectiveRate: number; feeCents: number } {
    if (fromCurrency === toCurrency) {
      return { convertedAmountCents: amountCents, effectiveRate: 1.0, feeCents: 0 };
    }

    const key = `${fromCurrency}:${toCurrency}`;
    const pair = this.BASE_RATES.get(key);

    if (!pair) {
      throw new Error(`Unsupported currency conversion pair: ${fromCurrency} to ${toCurrency}`);
    }

    const spreadMultiplier = 1 + pair.spreadBasisPoints / 10000;
    const effectiveRate = pair.rate * spreadMultiplier;
    const converted = Math.round(amountCents * effectiveRate);
    const fee = Math.round(amountCents * (pair.spreadBasisPoints / 10000));

    return {
      convertedAmountCents: converted,
      effectiveRate: Math.round(effectiveRate * 10000) / 10000,
      feeCents: fee
    };
  }
}
""")

    # 2. Notification Multi-Channel Delivery Router
    write_file("services/notification-service/src/domain/delivery-router.ts", """import { NotificationChannel } from '@novacommerce/core-types';

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
""")

    print("Production V6 modules generated.")

if __name__ == "__main__":
    generate_prod_v6()
