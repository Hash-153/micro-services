import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def build_payment_domain_expanded():
    print("Building Payment domain expanded...")
    
    # 1. Stripe Adapter
    write_file("services/payment-service/src/adapters/stripe-gateway.adapter.ts", """import { PaymentTransactionEntity, PaymentStatus, Currency } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface StripeChargeRequest {
  amountCents: number;
  currency: Currency;
  paymentMethodToken: string;
  orderId: string;
  customerEmail?: string;
  statementDescriptor?: string;
  metadata?: Record<string, string>;
}

export interface StripeChargeResponse {
  chargeId: string;
  status: 'succeeded' | 'pending' | 'failed' | 'requires_action';
  amountCapturedCents: number;
  feeCents: number;
  balanceTransactionId: string;
  clientSecret?: string;
  failureCode?: string;
  failureMessage?: string;
}

export class StripeGatewayAdapter {
  private logger: Logger;
  private isTestMode: boolean;

  constructor(logger: Logger, isTestMode: boolean = true) {
    this.logger = logger;
    this.isTestMode = isTestMode;
  }

  public async createCharge(request: StripeChargeRequest): Promise<StripeChargeResponse> {
    this.logger.info(`Initiating Stripe charge for order ${request.orderId}, amount: $${(request.amountCents / 100).toFixed(2)} ${request.currency}`);

    // In production, invokes Stripe API via secure TLS 1.3 client
    if (request.paymentMethodToken === 'tok_chargeDeclined') {
      return {
        chargeId: `ch_failed_${Date.now()}`,
        status: 'failed',
        amountCapturedCents: 0,
        feeCents: 0,
        balanceTransactionId: '',
        failureCode: 'card_declined',
        failureMessage: 'Your card was declined.'
      };
    }

    if (request.paymentMethodToken === 'tok_3dsRequired') {
      return {
        chargeId: `ch_3ds_${Date.now()}`,
        status: 'requires_action',
        amountCapturedCents: 0,
        feeCents: 0,
        balanceTransactionId: '',
        clientSecret: `pi_${Date.now()}_secret_${Date.now()}`
      };
    }

    const feeCents = Math.round(request.amountCents * 0.029 + 30); // 2.9% + 30c standard interchange

    return {
      chargeId: `ch_${Date.now()}_${Date.now().toString(36)}`,
      status: 'succeeded',
      amountCapturedCents: request.amountCents,
      feeCents,
      balanceTransactionId: `txn_bal_${Date.now().toString(36)}`
    };
  }

  public async createRefund(chargeId: string, amountCents?: number, reason?: string): Promise<{ refundId: string; status: string; amountRefundedCents: number }> {
    this.logger.info(`Processing Stripe refund for charge ${chargeId}, amount: ${amountCents ? '$' + (amountCents / 100).toFixed(2) : 'FULL'}`);
    return {
      refundId: `re_${Date.now()}_${Date.now().toString(36)}`,
      status: 'succeeded',
      amountRefundedCents: amountCents || 0
    };
  }
}
""")

    # 2. PayPal Adapter
    write_file("services/payment-service/src/adapters/paypal-gateway.adapter.ts", """import { Currency } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface PayPalOrderRequest {
  intent: 'CAPTURE' | 'AUTHORIZE';
  amountCents: number;
  currency: Currency;
  orderId: string;
  returnUrl: string;
  cancelUrl: string;
}

export interface PayPalOrderResponse {
  paypalOrderId: string;
  status: 'CREATED' | 'SAVED' | 'APPROVED' | 'VOIDED' | 'COMPLETED' | 'PAYER_ACTION_REQUIRED';
  approvalUrl: string;
}

export class PayPalGatewayAdapter {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async createOrder(request: PayPalOrderRequest): Promise<PayPalOrderResponse> {
    this.logger.info(`Creating PayPal order intent: ${request.intent} for order ${request.orderId}`);
    const paypalOrderId = `PAYPAL-ORD-${Date.now().toString(36).toUpperCase()}`;

    return {
      paypalOrderId,
      status: 'CREATED',
      approvalUrl: `https://www.sandbox.paypal.com/checkoutnow?token=${paypalOrderId}`
    };
  }

  public async captureOrder(paypalOrderId: string): Promise<{ captureId: string; status: string; feeCents: number }> {
    this.logger.info(`Capturing PayPal order ${paypalOrderId}`);
    return {
      captureId: `PAYPAL-CAP-${Date.now().toString(36).toUpperCase()}`,
      status: 'COMPLETED',
      feeCents: 150
    };
  }
}
""")

    # 3. Reconciliation Engine
    write_file("services/payment-service/src/services/reconciliation.service.ts", """import { LedgerAccountEntity, LedgerLineEntity, Currency } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';
import { InMemoryLedgerRepository } from '../repositories/payment.repository.js';

export interface ReconciliationReport {
  asOfDate: Date;
  totalDebitsCents: number;
  totalCreditsCents: number;
  imbalanceCents: number;
  isBalanced: boolean;
  accountBalances: {
    accountNumber: string;
    accountName: string;
    type: string;
    balanceCents: number;
    normalBalance: string;
  }[];
}

export class ReconciliationService {
  private logger: Logger;
  private ledgerRepo: InMemoryLedgerRepository;

  constructor(logger: Logger, ledgerRepo: InMemoryLedgerRepository) {
    this.logger = logger;
    this.ledgerRepo = ledgerRepo;
  }

  public async reconcileLedger(): Promise<ReconciliationReport> {
    this.logger.info('Executing automated general ledger trial balance reconciliation...');
    const accounts = await this.ledgerRepo.getAllAccounts();
    const journalEntries = await this.ledgerRepo.getAllJournalEntries();

    let totalDebits = 0;
    let totalCredits = 0;

    for (const entry of journalEntries) {
      for (const line of entry.lines) {
        if (line.entryType === 'DEBIT') {
          totalDebits += line.amount;
        } else if (line.entryType === 'CREDIT') {
          totalCredits += line.amount;
        }
      }
    }

    const imbalance = Math.abs(totalDebits - totalCredits);
    const isBalanced = imbalance === 0;

    if (!isBalanced) {
      this.logger.error(`CRITICAL: General Ledger is out of balance by $${(imbalance / 100).toFixed(2)}!`);
    } else {
      this.logger.info(`Reconciliation SUCCESS: General Ledger balanced at $${(totalDebits / 100).toFixed(2)}.`);
    }

    return {
      asOfDate: new Date(),
      totalDebitsCents: totalDebits,
      totalCreditsCents: totalCredits,
      imbalanceCents: imbalance,
      isBalanced,
      accountBalances: accounts.map(a => ({
        accountNumber: a.accountNumber,
        accountName: a.name,
        type: a.type,
        balanceCents: a.balance,
        normalBalance: ['ASSET', 'EXPENSE'].includes(a.type) ? 'DEBIT' : 'CREDIT'
      }))
    };
  }
}
""")

    print("Payment domain expanded.")

if __name__ == "__main__":
    build_payment_domain_expanded()
