import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v14():
    print("Generating comprehensive Production V14 Modules...")

    # 1. Order Service Fraud Risk Scorer Middleware
    write_file("services/order-service/src/domain/order-fraud-evaluator.ts", """import { OrderEntity } from '@novacommerce/core-types';

export class OrderFraudEvaluator {
  public static evaluateRisk(order: OrderEntity): { riskScore: number; isFlagged: boolean; reasons: string[] } {
    const reasons: string[] = [];
    let score = 0;

    // High order value
    if (order.totalAmount.amount >= 200000) {
      score += 30;
      reasons.push('High value order (>$2,000)');
    }

    // Multiple high-quantity items
    const highQtyItems = order.items.filter(i => i.quantity > 5);
    if (highQtyItems.length > 0) {
      score += 20;
      reasons.push('Bulk unit quantities requested');
    }

    // Shipping and Billing country mismatch
    if (order.shippingAddress.countryCode !== order.billingAddress.countryCode) {
      score += 25;
      reasons.push('Cross-border shipping/billing country mismatch');
    }

    return {
      riskScore: score,
      isFlagged: score >= 50,
      reasons
    };
  }
}
""")

    # 2. Notification Inbound Email Webhook Parser (SendGrid / AWS SES Inbound)
    write_file("services/notification-service/src/domain/inbound-email-parser.ts", """export interface ParsedInboundEmail {
  fromAddress: string;
  toAddress: string;
  subject: string;
  plainTextContent: string;
  extractedTicketId?: string;
  hasAttachments: boolean;
  receivedAt: Date;
}

export class InboundEmailParser {
  public static parse(rawWebhookPayload: any): ParsedInboundEmail {
    const headers = rawWebhookPayload?.headers || {};
    const from = rawWebhookPayload?.from || headers?.From || '';
    const to = rawWebhookPayload?.to || headers?.To || '';
    const subject = rawWebhookPayload?.subject || headers?.Subject || '';
    const text = rawWebhookPayload?.text || rawWebhookPayload?.body || '';

    // Ticket ID regex pattern: e.g. [TICK-12345]
    const ticketMatch = subject.match(/\\[TICK-([A-Za-z0-9-]+)\\]/);
    const ticketId = ticketMatch ? ticketMatch[1] : undefined;

    return {
      fromAddress: from,
      toAddress: to,
      subject,
      plainTextContent: text,
      extractedTicketId: ticketId,
      hasAttachments: Array.isArray(rawWebhookPayload?.attachments) && rawWebhookPayload.attachments.length > 0,
      receivedAt: new Date()
    };
  }
}
""")

    print("Production V14 modules generated.")

if __name__ == "__main__":
    generate_prod_v14()
