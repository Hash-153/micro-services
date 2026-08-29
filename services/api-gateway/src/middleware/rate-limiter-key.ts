import { Request } from 'express';

export class RateLimiterKeyGenerator {
  public static generateKey(req: Request): string {
    const authHeader = req.headers['authorization'];
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      // Use token suffix for key identification
      return `user_token:${token.slice(-16)}`;
    }

    const apiKey = req.headers['x-api-key'];
    if (apiKey && typeof apiKey === 'string') {
      return `api_key:${apiKey}`;
    }

    const ip = req.ip || req.socket.remoteAddress || '127.0.0.1';
    return `client_ip:${ip}`;
  }
}
