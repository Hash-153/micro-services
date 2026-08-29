import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v19():
    print("Generating comprehensive Production V19 Modules...")

    # 1. Fulfillment Service Carrier Webhook Signer & Verifier
    write_file("services/fulfillment-service/src/domain/carrier-webhook-verifier.ts", """import crypto from 'crypto';

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
""")

    # 2. Notification Service Email CSS Inliner
    write_file("services/notification-service/src/domain/email-css-inliner.ts", """export class EmailCssInliner {
  public static inlineStyles(htmlContent: string): string {
    // Basic inline transformation for bulletproof HTML emails
    return htmlContent
      .replace(/<p>/g, '<p style="margin: 0 0 16px; font-size: 15px; line-height: 1.5; color: #334155;">')
      .replace(/<h1>/g, '<h1 style="margin: 0 0 20px; font-size: 24px; font-weight: 700; color: #0f172a;">')
      .replace(/<h2>/g, '<h2 style="margin: 0 0 16px; font-size: 18px; font-weight: 600; color: #0f172a;">')
      .replace(/<a /g, '<a style="color: #2563eb; text-decoration: underline;" ')
      .replace(/<button>/g, '<button style="background-color: #2563eb; color: #ffffff; padding: 12px 24px; border-radius: 6px; font-weight: 600; border: none; cursor: pointer;">');
  }
}
""")

    print("Production V19 modules generated.")

if __name__ == "__main__":
    generate_prod_v19()
