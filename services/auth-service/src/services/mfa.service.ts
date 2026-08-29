import { createHmac, randomBytes } from 'crypto';

export interface MfaSetupResult {
  secret: string;
  otpauthUrl: string;
  backupCodes: string[];
}

export class MfaService {
  public static generateSecret(userEmail: string, issuer: string = 'NovaCommerce'): MfaSetupResult {
    const secret = randomBytes(20).toString('hex').toUpperCase().substring(0, 32);
    const otpauthUrl = `otpauth://totp/${encodeURIComponent(issuer)}:${encodeURIComponent(userEmail)}?secret=${secret}&issuer=${encodeURIComponent(issuer)}&algorithm=SHA1&digits=6&period=30`;
    
    const backupCodes: string[] = [];
    for (let i = 0; i < 8; i++) {
      backupCodes.push(randomBytes(4).toString('hex').toUpperCase());
    }

    return { secret, otpauthUrl, backupCodes };
  }

  public static verifyCode(secret: string, code: string, windowSteps: number = 1): boolean {
    if (!code || code.length !== 6 || !/^\d{6}$/.test(code)) {
      return false;
    }

    const epochTime = Math.floor(Date.now() / 1000);
    const stepSeconds = 30;
    const currentStep = Math.floor(epochTime / stepSeconds);

    for (let stepOffset = -windowSteps; stepOffset <= windowSteps; stepOffset++) {
      const step = currentStep + stepOffset;
      const expectedCode = this.generateTotpForStep(secret, step);
      if (expectedCode === code) {
        return true;
      }
    }

    return false;
  }

  private static generateTotpForStep(secret: string, step: number): string {
    const buffer = Buffer.alloc(8);
    buffer.writeBigInt64BE(BigInt(step));
    const hmac = createHmac('sha1', Buffer.from(secret, 'utf-8'));
    hmac.update(buffer);
    const digest = hmac.digest();

    const offset = digest[digest.length - 1] & 0x0f;
    const binary =
      ((digest[offset] & 0x7f) << 24) |
      ((digest[offset + 1] & 0xff) << 16) |
      ((digest[offset + 2] & 0xff) << 8) |
      (digest[offset + 3] & 0xff);

    const otp = binary % 1000000;
    return otp.toString().padStart(6, '0');
  }
}
