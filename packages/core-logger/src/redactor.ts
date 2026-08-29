const SENSITIVE_KEYS = new Set([
  'password',
  'passwordhash',
  'token',
  'accesstoken',
  'refreshtoken',
  'secret',
  'jwtsecret',
  'creditcard',
  'cardnumber',
  'cvv',
  'cvc',
  'ssn',
  'authorization',
  'apikey',
  'mfastuff',
  'mfasecret'
]);

export class Redactor {
  public static redact(obj: unknown, depth: number = 0): unknown {
    if (depth > 8 || obj === null || obj === undefined) {
      return obj;
    }

    if (typeof obj === 'string') {
      return obj;
    }

    if (Array.isArray(obj)) {
      return obj.map(item => Redactor.redact(item, depth + 1));
    }

    if (typeof obj === 'object') {
      const result: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
        const lowerKey = key.toLowerCase().replace(/[^a-z0-9]/g, '');
        if (SENSITIVE_KEYS.has(lowerKey)) {
          result[key] = '[REDACTED]';
        } else if (typeof value === 'object' && value !== null) {
          result[key] = Redactor.redact(value, depth + 1);
        } else {
          result[key] = value;
        }
      }
      return result;
    }

    return obj;
  }
}
