import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class WafRuleEvaluator {
  private static readonly SQLI_REGEX = /(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\b|--|\/\*|;)/i;
  private static readonly XSS_REGEX = /(<script\b|javascript:|onerror=|onload=|eval\()/i;
  private static readonly PATH_TRAVERSAL_REGEX = /(\.\.\/|\.\.\\)/;

  public static middleware(logger: Logger) {
    return (req: Request, res: Response, next: NextFunction) => {
      const url = req.originalUrl || req.url;
      const bodyStr = req.body ? JSON.stringify(req.body) : '';

      // Check URL and Body against WAF signatures
      if (this.PATH_TRAVERSAL_REGEX.test(url)) {
        logger.warn(`WAF blocked Path Traversal attack from ${req.ip}: ${url}`);
        return res.status(403).json({ success: false, statusCode: 403, error: { code: 'ERR_WAF_BLOCKED', message: 'Forbidden request pattern detected.' } });
      }

      if (this.SQLI_REGEX.test(url) || this.SQLI_REGEX.test(bodyStr)) {
        logger.warn(`WAF blocked SQL Injection signature from ${req.ip}`);
        return res.status(403).json({ success: false, statusCode: 403, error: { code: 'ERR_WAF_BLOCKED', message: 'Forbidden request pattern detected.' } });
      }

      if (this.XSS_REGEX.test(url) || this.XSS_REGEX.test(bodyStr)) {
        logger.warn(`WAF blocked XSS signature from ${req.ip}`);
        return res.status(403).json({ success: false, statusCode: 403, error: { code: 'ERR_WAF_BLOCKED', message: 'Forbidden request pattern detected.' } });
      }

      next();
    };
  }
}
