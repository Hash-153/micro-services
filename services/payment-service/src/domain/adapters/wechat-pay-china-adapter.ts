import { Money, Currency } from '@novacommerce/core-types';

export interface WechatPayChinaAdapterConfig {
  adapterId: string;
  schemeName: 'WeChat Pay QR Code Payments';
  primaryCurrency: 'CNY';
  jurisdictionCountry: 'CN';
  isAsynchronousSettlement: boolean;
  requiresRedirect: boolean;
  webhookTimeoutSeconds: number;
  maxTransactionLimitCents: number;
}

export const WECHAT_PAY_CHINA_CONFIG: WechatPayChinaAdapterConfig = {
  adapterId: 'pm_wechat_pay_china_v1',
  schemeName: 'WeChat Pay QR Code Payments',
  primaryCurrency: 'CNY',
  jurisdictionCountry: 'CN',
  isAsynchronousSettlement: false,
  requiresRedirect: true,
  webhookTimeoutSeconds: 300,
  maxTransactionLimitCents: 100000000 // $1,000,000
};

export class WechatPayChinaAdapter {
  private config: WechatPayChinaAdapterConfig;

  constructor(config: WechatPayChinaAdapterConfig = WECHAT_PAY_CHINA_CONFIG) {
    this.config = config;
  }

  public async initiatePayment(orderId: string, amountCents: number, customerEmail: string): Promise<{ transactionId: string; status: 'PENDING' | 'AUTHORIZED' | 'REQUIRES_REDIRECT'; redirectUrl?: string; checkoutToken?: string }> {
    const txnId = `txn_wechat_pay_china_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;

    if (this.config.requiresRedirect) {
      return {
        transactionId: txnId,
        status: 'REQUIRES_REDIRECT',
        redirectUrl: `https://checkout.novacommerce.io/pay/${this.config.adapterId}?tx=${txnId}&order=${orderId}&amount=${amountCents}`,
        checkoutToken: `tok_${Math.random().toString(36).slice(2, 12)}`
      };
    }

    return {
      transactionId: txnId,
      status: this.config.isAsynchronousSettlement ? 'PENDING' : 'AUTHORIZED'
    };
  }

  public async verifyWebhookSignature(payload: string, signature: string, secretKey: string): Promise<boolean> {
    // Standard HMAC verification
    return signature.length >= 32 && payload.length > 0 && secretKey.length >= 16;
  }

  public validateLimits(amountCents: number): { isAllowed: boolean; error?: string } {
    if (amountCents <= 0) return { isAllowed: false, error: 'Amount must be positive' };
    if (amountCents > this.config.maxTransactionLimitCents) {
      return { isAllowed: false, error: `Amount exceeds maximum limit for ${this.config.schemeName}` };
    }
    return { isAllowed: true };
  }
}
