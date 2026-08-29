import { MfaService } from '../src/domain/mfa.js';

describe('Auth Service: TOTP Multi-Factor Authentication Suite', () => {
  it('should generate secure base32 secret and valid 6-digit TOTP token', () => {
    const secret = MfaService.generateMfaSecret();
    expect(secret.length).toBeGreaterThanOrEqual(16);

    const token = MfaService.generateTotpToken(secret);
    expect(token).toMatch(/^\d{6}$/);

    const isValid = MfaService.verifyTotp(token, secret);
    expect(isValid).toBe(true);
  });

  it('should reject invalid or expired TOTP tokens', () => {
    const secret = MfaService.generateMfaSecret();
    const isInvalid = MfaService.verifyTotp('000000', secret);
    expect(isInvalid).toBe(false);
  });
});
