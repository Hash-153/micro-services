import crypto from 'crypto';
import { Request, Response, NextFunction } from 'express';

export class PayloadDecryptionMiddleware {
  public static middleware(aesKeyBase64: string) {
    const key = Buffer.from(aesKeyBase64, 'base64');

    return (req: Request, res: Response, next: NextFunction) => {
      const isEncrypted = req.headers['x-payload-encryption'] === 'AES-256-GCM';
      if (!isEncrypted || !req.body?.encryptedData) {
        return next();
      }

      try {
        const { encryptedData, iv, authTag } = req.body;
        const decipher = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(iv, 'base64'));
        decipher.setAuthTag(Buffer.from(authTag, 'base64'));

        let decrypted = decipher.update(encryptedData, 'base64', 'utf8');
        decrypted += decipher.final('utf8');

        req.body = JSON.parse(decrypted);
        next();
      } catch (err) {
        return res.status(400).json({
          success: false,
          statusCode: 400,
          error: { code: 'ERR_DECRYPTION_FAILED', message: 'Failed to decrypt secure payload.' }
        });
      }
    };
  }
}
