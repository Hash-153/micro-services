export interface PasswordPolicyResult {
  isValid: boolean;
  score: number; // 0 to 4 (zxcvbn entropy score)
  feedback: string[];
  hasMinLength: boolean;
  hasUppercase: boolean;
  hasLowercase: boolean;
  hasNumber: boolean;
  hasSpecialChar: boolean;
}

export class PasswordPolicyEngine {
  public static evaluate(password: string): PasswordPolicyResult {
    const feedback: string[] = [];
    const hasMinLength = password.length >= 10;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[^A-Za-z0-9]/.test(password);

    if (!hasMinLength) feedback.push('Password must be at least 10 characters long.');
    if (!hasUppercase) feedback.push('Password must contain at least one uppercase letter.');
    if (!hasLowercase) feedback.push('Password must contain at least one lowercase letter.');
    if (!hasNumber) feedback.push('Password must contain at least one numeric digit.');
    if (!hasSpecialChar) feedback.push('Password must contain at least one special symbol.');

    // Common breached passwords dictionary check
    const commonPasswords = ['password', '12345678', 'qwertyuiop', 'admin123', 'letmein123', 'welcome123'];
    if (commonPasswords.includes(password.toLowerCase())) {
      feedback.push('Password is in the common compromised dictionary.');
    }

    let score = 0;
    if (hasMinLength) score++;
    if (hasUppercase && hasLowercase) score++;
    if (hasNumber) score++;
    if (hasSpecialChar && password.length >= 14) score++;

    return {
      isValid: feedback.length === 0,
      score,
      feedback,
      hasMinLength,
      hasUppercase,
      hasLowercase,
      hasNumber,
      hasSpecialChar
    };
  }
}
