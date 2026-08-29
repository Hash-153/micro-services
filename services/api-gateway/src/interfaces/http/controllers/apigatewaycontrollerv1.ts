import { Request, Response } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ApiGatewayRepositoryV1 } from '../repositories/apigatewayrepositoryv1.js';

export class ApiGatewayControllerV1 {
  private repo: ApiGatewayRepositoryV1;
  private logger: Logger;

  constructor(repo: ApiGatewayRepositoryV1, logger: Logger) {
    this.repo = repo;
    this.logger = logger;
  }

  public async getById(req: Request, res: Response): Promise<Response> {
    const { id } = req.params;
    if (!id || id.length < 10) {
      return res.status(400).json({ success: false, statusCode: 400, error: { code: 'ERR_INVALID_ID', message: 'Entity ID parameter is malformed.' } });
    }

    try {
      const item = await this.repo.findById(id);
      if (!item) {
        return res.status(404).json({ success: false, statusCode: 404, error: { code: 'ERR_NOT_FOUND', message: 'Entity not found.' } });
      }
      return res.status(200).json({ success: true, statusCode: 200, data: item });
    } catch (err: any) {
      this.logger.error(`Error in ApiGatewayControllerV1.getById:`, err);
      return res.status(500).json({ success: false, statusCode: 500, error: { code: 'ERR_INTERNAL_SERVER', message: err.message } });
    }
  }

  public async listByTenant(req: Request, res: Response): Promise<Response> {
    const tenantId = (req.headers['x-tenant-id'] as string) || (req.query.tenantId as string);
    if (!tenantId) {
      return res.status(400).json({ success: false, statusCode: 400, error: { code: 'ERR_MISSING_TENANT', message: 'x-tenant-id header required.' } });
    }

    const limit = Math.min(100, parseInt(req.query.limit as string || '20', 10));
    const offset = Math.max(0, parseInt(req.query.offset as string || '0', 10));

    try {
      const items = await this.repo.findByTenant(tenantId, limit, offset);
      return res.status(200).json({ success: true, statusCode: 200, data: { items, limit, offset, count: items.length } });
    } catch (err: any) {
      this.logger.error(`Error in ApiGatewayControllerV1.listByTenant:`, err);
      return res.status(500).json({ success: false, statusCode: 500, error: { code: 'ERR_INTERNAL_SERVER', message: err.message } });
    }
  }

  public async create(req: Request, res: Response): Promise<Response> {
    const { id, tenantId, entityCode, displayName, status, metadata } = req.body;
    if (!tenantId || !entityCode || !displayName) {
      return res.status(400).json({ success: false, statusCode: 400, error: { code: 'ERR_VALIDATION', message: 'tenantId, entityCode, and displayName are required fields.' } });
    }

    try {
      const created = await this.repo.create({
        id: id || `ent_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
        tenantId,
        entityCode,
        displayName,
        status: status || 'ACTIVE',
        metadata: metadata || {},
        isDeleted: false
      });
      return res.status(201).json({ success: true, statusCode: 201, data: created });
    } catch (err: any) {
      this.logger.error(`Error in ApiGatewayControllerV1.create:`, err);
      return res.status(500).json({ success: false, statusCode: 500, error: { code: 'ERR_INTERNAL_SERVER', message: err.message } });
    }
  }
}
