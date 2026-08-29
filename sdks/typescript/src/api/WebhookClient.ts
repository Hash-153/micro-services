import { NovaCommerceHttpClient } from '../client/NovaCommerceHttpClient.js';

export interface WebhookClientFilterOptions {
  page?: number;
  limit?: number;
  search?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  [key: string]: any;
}

export class WebhookClient {
  private http: NovaCommerceHttpClient;
  private readonly basePath: string = '/api/v1/webhooks';

  constructor(http: NovaCommerceHttpClient) {
    this.http = http;
  }

  public async getById<T = any>(id: string): Promise<T> {
    const response = await this.http.get<T>(`${this.basePath}/${id}`);
    return response.data;
  }

  public async list<T = any>(options?: WebhookClientFilterOptions): Promise<{ items: T[]; total: number; page: number; limit: number }> {
    const response = await this.http.get<any>(this.basePath, options);
    return response.data;
  }

  public async create<T = any>(payload: Record<string, any>): Promise<T> {
    const response = await this.http.post<T>(this.basePath, payload);
    return response.data;
  }

  public async update<T = any>(id: string, payload: Record<string, any>): Promise<T> {
    const response = await this.http.put<T>(`${this.basePath}/${id}`, payload);
    return response.data;
  }

  public async patch<T = any>(id: string, payload: Record<string, any>): Promise<T> {
    const response = await this.http.patch<T>(`${this.basePath}/${id}`, payload);
    return response.data;
  }

  public async delete(id: string): Promise<boolean> {
    const response = await this.http.delete<boolean>(`${this.basePath}/${id}`);
    return Boolean(response.data);
  }
}
