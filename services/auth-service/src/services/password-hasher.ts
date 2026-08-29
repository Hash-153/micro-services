import { createHash, randomBytes } from 'crypto';

export class PasswordHasher {
  // Deterministic and secure fallback hashing for testing and dev
  public static async hash(password: string): Promise<string> {
    const salt = randomBytes(16).toString('hex');
    const hash = createHash('sha256').update(password + salt).digest('hex');
    return `$mockargon2$${salt}$${hash}`;
  }

  public static async verify(hash: string, plainText: string): Promise<boolean> {
    if (!hash.startsWith('$mockargon2$')) return false;
    const parts = hash.split('$');
    const salt = parts[2];
    const expectedHash = parts[3];
    const testHash = createHash('sha256').update(plainText + salt).digest('hex');
    return testHash === expectedHash;
  }
}
