import { PaymentTransactionEntity, Money } from '@novacommerce/core-types';

export interface PaymentRequest {
  orderId: string;
  userId: string;
  amount: Money;
  methodType: 'CREDIT_CARD' | 'DEBIT_CARD' | 'BANK_TRANSFER' | 'PAYPAL' | 'APPLE_PAY' | 'GOOGLE_PAY' | 'STORE_CREDIT';
  paymentDetails: {
    cardNumber?: string;
    cardExpiry?: string;
    cardCvv?: string;
    bankAccountNumber?: string;
    routingNumber?: string;
    paypalEmail?: string;
    applePayToken?: string;
    googlePayToken?: string;
    storeCreditId?: string;
  };
  idempotencyKey: string;
}

export interface PaymentResult {
  success: boolean;
  transactionId?: string;
  providerTransactionId?: string;
  failureReason?: string;
  processedAt: Date;
}

export interface RefundRequest {
  transactionId: string;
  amount?: Money;
  reason: string;
  idempotencyKey: string;
}

export interface RefundResult {
  success: boolean;
  refundTransactionId?: string;
  providerRefundId?: string;
  failureReason?: string;
  processedAt: Date;
}

export class PaymentProcessor {
  private transactions: Map<string, PaymentTransactionEntity> = new Map();

  public async processPayment(request: PaymentRequest): Promise<PaymentResult> {
    // Check idempotency
    const existing = this.findTransactionByIdempotencyKey(request.idempotencyKey);
    if (existing) {
      return {
        success: existing.status === 'COMPLETED',
        transactionId: existing.transactionReference,
        providerTransactionId: existing.providerTransactionId,
        failureReason: existing.failureReason || undefined,
        processedAt: existing.createdAt
      };
    }

    // Process payment based on method type
    let result: PaymentResult;
    switch (request.methodType) {
      case 'CREDIT_CARD':
      case 'DEBIT_CARD':
        result = await this.processCardPayment(request);
        break;
      case 'PAYPAL':
        result = await this.processPayPalPayment(request);
        break;
      case 'APPLE_PAY':
        result = await this.processApplePayPayment(request);
        break;
      case 'GOOGLE_PAY':
        result = await this.processGooglePayPayment(request);
        break;
      case 'STORE_CREDIT':
        result = await this.processStoreCreditPayment(request);
        break;
      default:
        result = {
          success: false,
          failureReason: 'Unsupported payment method',
          processedAt: new Date()
        };
    }

    // Create transaction record
    const transaction: PaymentTransactionEntity = {
      id: `txn-${Date.now()}`,
      transactionReference: result.transactionId || `TXN-${Date.now()}`,
      orderId: request.orderId,
      userId: request.userId,
      amount: request.amount,
      status: result.success ? 'COMPLETED' : 'FAILED',
      methodType: request.methodType,
      provider: this.getProviderForMethod(request.methodType),
      providerTransactionId: result.providerTransactionId,
      failureReason: result.failureReason,
      idempotencyKey: request.idempotencyKey,
      metadata: {
        paymentDetails: this.sanitizePaymentDetails(request.paymentDetails)
      },
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.transactions.set(transaction.id, transaction);

    return result;
  }

  private async processCardPayment(request: PaymentRequest): Promise<PaymentResult> {
    // Simulate card payment processing
    const isValidCard = this.validateCardDetails(request.paymentDetails);

    if (!isValidCard) {
      return {
        success: false,
        failureReason: 'Invalid card details',
        processedAt: new Date()
      };
    }

    // Simulate processing delay
    await this.simulateProcessingDelay(500);

    return {
      success: true,
      transactionId: `CARD-${Date.now()}`,
      providerTransactionId: `STRIPE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processPayPalPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.paypalEmail) {
      return {
        success: false,
        failureReason: 'PayPal email required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(800);

    return {
      success: true,
      transactionId: `PAYPAL-${Date.now()}`,
      providerTransactionId: `PAYPAL-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processApplePayPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.applePayToken) {
      return {
        success: false,
        failureReason: 'Apple Pay token required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(400);

    return {
      success: true,
      transactionId: `APPLE-${Date.now()}`,
      providerTransactionId: `APPLE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processGooglePayPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.googlePayToken) {
      return {
        success: false,
        failureReason: 'Google Pay token required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(450);

    return {
      success: true,
      transactionId: `GOOGLE-${Date.now()}`,
      providerTransactionId: `GOOGLE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processStoreCreditPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.storeCreditId) {
      return {
        success: false,
        failureReason: 'Store credit ID required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(200);

    return {
      success: true,
      transactionId: `CREDIT-${Date.now()}`,
      providerTransactionId: `INTERNAL-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  public async processRefund(request: RefundRequest): Promise<RefundResult> {
    const transaction = this.transactions.get(request.transactionId);
    if (!transaction) {
      return {
        success: false,
        failureReason: 'Transaction not found',
        processedAt: new Date()
      };
    }

    if (transaction.status !== 'COMPLETED') {
      return {
        success: false,
        failureReason: 'Cannot refund non-completed transaction',
        processedAt: new Date()
      };
    }

    // Check idempotency
    const existing = this.findTransactionByIdempotencyKey(request.idempotencyKey);
    if (existing) {
      return {
        success: existing.status === 'REFUNDED',
        refundTransactionId: existing.transactionReference,
        providerRefundId: existing.providerTransactionId,
        failureReason: existing.failureReason || undefined,
        processedAt: existing.createdAt
      };
    }

    await this.simulateProcessingDelay(1000);

    const refundTransactionId = `REFUND-${Date.now()}`;
    const providerRefundId = `${transaction.provider}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;

    // Create refund transaction record
    const refundTransaction: PaymentTransactionEntity = {
      id: `txn-${Date.now()}`,
      transactionReference: refundTransactionId,
      orderId: transaction.orderId,
      userId: transaction.userId,
      amount: request.amount || transaction.amount,
      status: 'REFUNDED',
      methodType: transaction.methodType,
      provider: transaction.provider,
      providerTransactionId: providerRefundId,
      idempotencyKey: request.idempotencyKey,
      metadata: {
        originalTransactionId: transaction.transactionReference,
        refundReason: request.reason
      },
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.transactions.set(refundTransaction.id, refundTransaction);

    return {
      success: true,
      refundTransactionId,
      providerRefundId,
      processedAt: new Date()
    };
  }

  private validateCardDetails(details: any): boolean {
    // Basic validation - in production, this would use proper card validation
    const cardNumber = details.cardNumber?.replace(/\s+/g, '');
    return !!(cardNumber && cardNumber.length >= 13 && cardNumber.length <= 19);
  }

  private sanitizePaymentDetails(details: any): any {
    // Remove sensitive data from payment details
    const sanitized = { ...details };
    if (sanitized.cardNumber) {
      sanitized.cardNumber = this.maskCardNumber(sanitized.cardNumber);
    }
    if (sanitized.cardCvv) {
      delete sanitized.cardCvv;
    }
    return sanitized;
  }

  private maskCardNumber(cardNumber: string): string {
    const cleaned = cardNumber.replace(/\s/g, '');
    if (cleaned.length <= 4) return '****';
    return '****' + cleaned.slice(-4);
  }

  private getProviderForMethod(methodType: string): 'STRIPE' | 'PAYPAL' | 'ADYEN' | 'MOCK' | 'INTERNAL_LEDGER' {
    switch (methodType) {
      case 'CREDIT_CARD':
      case 'DEBIT_CARD':
      case 'APPLE_PAY':
      case 'GOOGLE_PAY':
        return 'STRIPE';
      case 'PAYPAL':
        return 'PAYPAL';
      case 'STORE_CREDIT':
        return 'INTERNAL_LEDGER';
      default:
        return 'MOCK';
    }
  }

  private findTransactionByIdempotencyKey(key: string): PaymentTransactionEntity | undefined {
    return Array.from(this.transactions.values()).find(t => t.idempotencyKey === key);
  }

  private simulateProcessingDelay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  public async getTransaction(transactionId: string): Promise<PaymentTransactionEntity | null> {
    return this.transactions.get(transactionId) || null;
  }

  public async getTransactionsByOrder(orderId: string): Promise<PaymentTransactionEntity[]> {
    return Array.from(this.transactions.values()).filter(t => t.orderId === orderId);
  }

  public async getTransactionsByUser(userId: string): Promise<PaymentTransactionEntity[]> {
    return Array.from(this.transactions.values()).filter(t => t.userId === userId);
  }
}
