import { Logger } from '@novacommerce/core-logger';

export interface SmsDispatchOptions {
  toPhoneNumber: string;
  messageBody: string;
  senderId?: string;
}

export class SmsDispatcher {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async dispatch(options: SmsDispatchOptions): Promise<{ messageId: string; status: 'DELIVERED' | 'QUEUED' }> {
    this.logger.info(`Dispatching SMS to ${options.toPhoneNumber}`);
    
    // In production, sends via Twilio / AWS SNS
    const messageId = `msg_sms_${Date.now().toString(36)}`;
    return {
      messageId,
      status: 'DELIVERED'
    };
  }
}
