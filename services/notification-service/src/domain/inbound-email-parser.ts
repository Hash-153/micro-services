export interface ParsedInboundEmail {
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
    const ticketMatch = subject.match(/\[TICK-([A-Za-z0-9-]+)\]/);
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
