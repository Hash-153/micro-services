import crypto from 'crypto';

export class CarrierWebhookVerifier {
  public static verifyFedExSignature(rawBody: string, signatureHeader: string, secretKey: string): boolean {
    const computed = crypto
      .createHmac('sha256', secretKey)
      .update(rawBody, 'utf8')
      .digest('hex');

    return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(signatureHeader));
  }

  public static verifyUpsSignature(rawBody: string, signatureHeader: string, secretKey: string): boolean {
    const computed = crypto
      .createHmac('sha256', secretKey)
      .update(rawBody, 'utf8')
      .digest('base64');

    return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(signatureHeader));
  }
}
