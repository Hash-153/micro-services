import crypto from 'crypto';

export class PciAuditLogEncryptor {
  public static encryptLogPayload(plainTextJson: string, masterKeyHex: string): { ivHex: string; encryptedDataHex: string; authTagHex: string } {
    const key = Buffer.from(masterKeyHex, 'hex');
    const iv = crypto.randomBytes(12); // 96-bit IV for AES-GCM
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

    let encrypted = cipher.update(plainTextJson, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag();

    return {
      ivHex: iv.toString('hex'),
      encryptedDataHex: encrypted,
      authTagHex: authTag.toString('hex')
    };
  }

  public static decryptLogPayload(encryptedDataHex: string, ivHex: string, authTagHex: string, masterKeyHex: string): string {
    const key = Buffer.from(masterKeyHex, 'hex');
    const iv = Buffer.from(ivHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');

    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encryptedDataHex, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}
