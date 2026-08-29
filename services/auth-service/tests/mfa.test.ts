import { MfaService } from '../src/services/mfa.service.js';

describe('MFA TOTP Suite', () => {
  it('should generate valid secret and backup codes', () => {
    const setup = MfaService.generateSecret('user@novacommerce.io');
    expect(setup.secret.length).toBeGreaterThanOrEqual(16);
    expect(setup.otpauthUrl).toContain('otpauth://totp/');
    expect(setup.backupCodes.length).toBe(8);
  });
});
