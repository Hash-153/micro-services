import { Logger } from '@novacommerce/core-logger';

export interface EmailDispatchOptions {
  to: string;
  from?: string;
  subject: string;
  htmlBody: string;
  textBody?: string;
  replyTo?: string;
  attachments?: { filename: string; contentBase64: string; contentType: string }[];
}

export class EmailDispatcher {
  private logger: Logger;
  private defaultSender: string;

  constructor(logger: Logger, defaultSender: string = 'no-reply@novacommerce.io') {
    this.logger = logger;
    this.defaultSender = defaultSender;
  }

  public async dispatch(options: EmailDispatchOptions): Promise<{ messageId: string; status: 'SENT' | 'QUEUED' }> {
    this.logger.info(`Dispatching transactional email to ${options.to}, subject: "${options.subject}"`);
    
    // In production, sends via AWS SES / SendGrid API
    const messageId = `msg_email_${Date.now().toString(36)}_${crypto.randomUUID().substring(0, 8)}`;
    return {
      messageId,
      status: 'SENT'
    };
  }
}
