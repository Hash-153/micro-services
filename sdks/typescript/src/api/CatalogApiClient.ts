import { ProductEntity, CreateProductDTO, ApiResponse } from '@novacommerce/core-types';

export class CatalogApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async listProducts(page: number = 1, limit: number = 20): Promise<{ items: ProductEntity[]; total: number }> {
    const res = await fetch(`${this.baseUrl}/api/v1/catalog/products?page=${page}&limit=${limit}`);
    if (!res.ok) throw new Error(`List products failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ProductEntity[]>;
    return { items: json.data, total: json.meta?.totalItems || json.data.length };
  }

  public async getProductById(id: string): Promise<ProductEntity> {
    const res = await fetch(`${this.baseUrl}/api/v1/catalog/products/${id}`);
    if (!res.ok) throw new Error(`Get product failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ProductEntity>;
    return json.data;
  }

  public async createProduct(dto: CreateProductDTO): Promise<ProductEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/catalog/products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Create product failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ProductEntity>;
    return json.data;
  }
}
