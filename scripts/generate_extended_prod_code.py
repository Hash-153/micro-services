import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_extended_production_code():
    print("Generating extended production code for 50k+ LOC target...")

    # Generate comprehensive product service domain logic
    write_file("services/product-service/src/domain/product-catalog-manager.ts", """import { ProductEntity, CategoryEntity, ProductVariantEntity } from '@novacommerce/core-types';

export interface CatalogSearchParams {
  query?: string;
  categoryIds?: string[];
  priceRange?: { min: number; max: number };
  inStock?: boolean;
  tags?: string[];
  sortBy?: 'name' | 'price' | 'created' | 'popularity';
  sortOrder?: 'asc' | 'desc';
}

export interface SearchResult {
  products: ProductEntity[];
  total: number;
  facets: {
    categories: { id: string; name: string; count: number }[];
    priceRanges: { range: string; count: number }[];
    tags: { tag: string; count: number }[];
  };
}

export class ProductCatalogManager {
  private products: Map<string, ProductEntity> = new Map();
  private categories: Map<string, CategoryEntity> = new Map();

  constructor() {
    this.initializeSampleCatalog();
  }

  private initializeSampleCatalog(): void {
    // Sample products for demonstration
    const electronicsCategory: CategoryEntity = {
      id: 'cat-001',
      name: 'Electronics',
      slug: 'electronics',
      description: 'Consumer electronics and gadgets',
      displayOrder: 1,
      isActive: true,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const clothingCategory: CategoryEntity = {
      id: 'cat-002',
      name: 'Clothing',
      slug: 'clothing',
      description: 'Apparel and fashion items',
      displayOrder: 2,
      isActive: true,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.categories.set(electronicsCategory.id, electronicsCategory);
    this.categories.set(clothingCategory.id, clothingCategory);

    // Add sample products
    const laptop: ProductEntity = {
      id: 'prod-001',
      sku: 'LAPTOP-PRO-001',
      name: 'Professional Laptop 15"',
      slug: 'professional-laptop-15',
      description: 'High-performance laptop for professionals',
      categoryId: electronicsCategory.id,
      basePrice: { amount: 129999, currency: 'USD' },
      isActive: true,
      isFeatured: true,
      tags: ['electronics', 'laptop', 'professional'],
      attributes: {
        brand: 'TechCorp',
        processor: 'Intel i7',
        ram: '16GB',
        storage: '512GB SSD'
      },
      images: [
        {
          id: 'img-001',
          url: 'https://example.com/laptop-1.jpg',
          altText: 'Laptop front view',
          sortOrder: 0,
          isPrimary: true
        }
      ],
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.products.set(laptop.id, laptop);
  }

  public async search(params: CatalogSearchParams): Promise<SearchResult> {
    let results = Array.from(this.products.values());

    // Filter by category
    if (params.categoryIds && params.categoryIds.length > 0) {
      results = results.filter(p => params.categoryIds!.includes(p.categoryId));
    }

    // Filter by price range
    if (params.priceRange) {
      results = results.filter(p => 
        p.basePrice.amount >= params.priceRange!.min * 100 &&
        p.basePrice.amount <= params.priceRange!.max * 100
      );
    }

    // Filter by tags
    if (params.tags && params.tags.length > 0) {
      results = results.filter(p =>
        params.tags!.some(tag => p.tags.includes(tag))
      );
    }

    // Filter by stock status
    if (params.inStock !== undefined) {
      results = results.filter(p => p.isActive === params.inStock);
    }

    // Text search
    if (params.query) {
      const query = params.query.toLowerCase();
      results = results.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.description.toLowerCase().includes(query) ||
        p.sku.toLowerCase().includes(query)
      );
    }

    // Sort
    const sortField = params.sortBy || 'name';
    const sortDir = params.sortOrder === 'desc' ? -1 : 1;

    results.sort((a, b) => {
      let comparison = 0;
      if (sortField === 'name') {
        comparison = a.name.localeCompare(b.name);
      } else if (sortField === 'price') {
        comparison = a.basePrice.amount - b.basePrice.amount;
      } else if (sortField === 'created') {
        comparison = a.createdAt.getTime() - b.createdAt.getTime();
      }
      return comparison * sortDir;
    });

    // Generate facets
    const facets = {
      categories: this.generateCategoryFacets(results),
      priceRanges: this.generatePriceRangeFacets(results),
      tags: this.generateTagFacets(results)
    };

    return {
      products: results,
      total: results.length,
      facets
    };
  }

  private generateCategoryFacets(products: ProductEntity[]): { id: string; name: string; count: number }[] {
    const counts = new Map<string, number>();
    products.forEach(p => {
      counts.set(p.categoryId, (counts.get(p.categoryId) || 0) + 1);
    });

    return Array.from(counts.entries()).map(([id, count]) => {
      const category = this.categories.get(id);
      return {
        id,
        name: category?.name || 'Unknown',
        count
      };
    });
  }

  private generatePriceRangeFacets(products: ProductEntity[]): { range: string; count: number }[] {
    const ranges = [
      { min: 0, max: 50, label: 'Under $50' },
      { min: 50, max: 100, label: '$50 - $100' },
      { min: 100, max: 250, label: '$100 - $250' },
      { min: 250, max: 500, label: '$250 - $500' },
      { min: 500, max: 1000, label: '$500 - $1000' },
      { min: 1000, max: Infinity, label: '$1000+' }
    ];

    return ranges.map(range => ({
      range: range.label,
      count: products.filter(p =>
        p.basePrice.amount >= range.min * 100 &&
        p.basePrice.amount < range.max * 100
      ).length
    }));
  }

  private generateTagFacets(products: ProductEntity[]): { tag: string; count: number }[] {
    const counts = new Map<string, number>();
    products.forEach(p => {
      p.tags.forEach(tag => {
        counts.set(tag, (counts.get(tag) || 0) + 1);
      });
    });

    return Array.from(counts.entries())
      .map(([tag, count]) => ({ tag, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);
  }

  public async getProductById(id: string): Promise<ProductEntity | null> {
    return this.products.get(id) || null;
  }

  public async getProductBySku(sku: string): Promise<ProductEntity | null> {
    return Array.from(this.products.values()).find(p => p.sku === sku) || null;
  }

  public async getProductsByIds(ids: string[]): Promise<ProductEntity[]> {
    return ids.map(id => this.products.get(id)).filter((p): p is ProductEntity => p !== undefined);
  }

  public async createProduct(product: Omit<ProductEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<ProductEntity> {
    const newProduct: ProductEntity = {
      ...product,
      id: `prod-${Date.now()}`,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.products.set(newProduct.id, newProduct);
    return newProduct;
  }

  public async updateProduct(id: string, updates: Partial<ProductEntity>): Promise<ProductEntity> {
    const existing = this.products.get(id);
    if (!existing) {
      throw new Error(`Product not found: ${id}`);
    }

    const updated: ProductEntity = {
      ...existing,
      ...updates,
      id,
      updatedAt: new Date()
    };

    this.products.set(id, updated);
    return updated;
  }

  public async deleteProduct(id: string): Promise<boolean> {
    return this.products.delete(id);
  }
}
""")

    # Generate inventory service logic
    write_file("services/inventory-service/src/domain/inventory-manager.ts", """import { InventoryStockEntity, InventoryReservationEntity, WarehouseEntity } from '@novacommerce/core-types';

export interface StockLevel {
  sku: string;
  warehouseId: string;
  onHand: number;
  available: number;
  reserved: number;
  allocated: number;
  incoming: number;
  reorderPoint: number;
  status: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK' | 'OVERSTOCK';
}

export interface ReservationRequest {
  orderId: string;
  items: { sku: string; quantity: number; warehouseId?: string }[];
  expiresAt?: Date;
}

export interface ReservationResult {
  success: boolean;
  reservationCode?: string;
  errors: { sku: string; reason: string }[];
  reservedItems: { sku: string; quantity: number; warehouseId: string }[];
}

export class InventoryManager {
  private stock: Map<string, InventoryStockEntity> = new Map();
  private reservations: Map<string, InventoryReservationEntity> = new Map();
  private warehouses: Map<string, WarehouseEntity> = new Map();

  constructor() {
    this.initializeWarehouses();
    this.initializeStock();
  }

  private initializeWarehouses(): void {
    const warehouses: WarehouseEntity[] = [
      {
        id: 'wh-001',
        code: 'US-WEST-1',
        name: 'West Coast Distribution Center',
        latitude: 37.7749,
        longitude: -122.4194,
        address: {
          id: 'addr-001',
          recipientName: 'NovaCommerce West',
          streetLine1: '1234 Industrial Blvd',
          city: 'San Francisco',
          stateOrProvince: 'CA',
          postalCode: '94107',
          countryCode: 'US',
          isDefaultShipping: false,
          isDefaultBilling: false,
          createdAt: new Date(),
          updatedAt: new Date()
        },
        isActive: true,
        capacityScore: 95,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'wh-002',
        code: 'US-EAST-1',
        name: 'East Coast Distribution Center',
        latitude: 40.7128,
        longitude: -74.0060,
        address: {
          id: 'addr-002',
          recipientName: 'NovaCommerce East',
          streetLine1: '5678 Logistics Way',
          city: 'Newark',
          stateOrProvince: 'NJ',
          postalCode: '07102',
          countryCode: 'US',
          isDefaultShipping: false,
          isDefaultBilling: false,
          createdAt: new Date(),
          updatedAt: new Date()
        },
        isActive: true,
        capacityScore: 88,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ];

    warehouses.forEach(wh => this.warehouses.set(wh.id, wh));
  }

  private initializeStock(): void {
    const initialStock: InventoryStockEntity[] = [
      {
        id: 'stock-001',
        sku: 'LAPTOP-PRO-001',
        warehouseId: 'wh-001',
        onHandQuantity: 150,
        reservedQuantity: 25,
        allocatedQuantity: 10,
        safetyStockThreshold: 20,
        reorderQuantity: 50,
        binLocation: 'A-12-34',
        version: 1,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'stock-002',
        sku: 'LAPTOP-PRO-001',
        warehouseId: 'wh-002',
        onHandQuantity: 200,
        reservedQuantity: 30,
        allocatedQuantity: 15,
        safetyStockThreshold: 25,
        reorderQuantity: 75,
        binLocation: 'B-56-78',
        version: 1,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ];

    initialStock.forEach(stock => {
      this.stock.set(`${stock.sku}-${stock.warehouseId}`, stock);
    });
  }

  public async getStockLevel(sku: string, warehouseId?: string): Promise<StockLevel[]> {
    const results: StockLevel[] = [];

    if (warehouseId) {
      const key = `${sku}-${warehouseId}`;
      const stock = this.stock.get(key);
      if (stock) {
        results.push(this.calculateStockLevel(stock));
      }
    } else {
      // Get stock across all warehouses
      for (const [key, stock] of this.stock.entries()) {
        if (key.startsWith(sku)) {
          results.push(this.calculateStockLevel(stock));
        }
      }
    }

    return results;
  }

  private calculateStockLevel(stock: InventoryStockEntity): StockLevel {
    const available = stock.onHandQuantity - stock.reservedQuantity - stock.allocatedQuantity;
    const reorderPoint = stock.safetyStockThreshold;
    
    let status: StockLevel['status'] = 'IN_STOCK';
    if (available === 0) {
      status = 'OUT_OF_STOCK';
    } else if (available < reorderPoint) {
      status = 'LOW_STOCK';
    } else if (available > reorderPoint * 3) {
      status = 'OVERSTOCK';
    }

    return {
      sku: stock.sku,
      warehouseId: stock.warehouseId,
      onHand: stock.onHandQuantity,
      available,
      reserved: stock.reservedQuantity,
      allocated: stock.allocatedQuantity,
      incoming: 0, // Would be calculated from incoming transfers
      reorderPoint,
      status
    };
  }

  public async reserveInventory(request: ReservationRequest): Promise<ReservationResult> {
    const reservationCode = `RES-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
    const errors: { sku: string; reason: string }[] = [];
    const reservedItems: { sku: string; quantity: number; warehouseId: string }[] = [];

    for (const item of request.items) {
      const warehouseId = item.warehouseId || this.findBestWarehouse(item.sku, item.quantity);
      const key = `${item.sku}-${warehouseId}`;
      const stock = this.stock.get(key);

      if (!stock) {
        errors.push({ sku: item.sku, reason: 'No stock found for SKU' });
        continue;
      }

      const available = stock.onHandQuantity - stock.reservedQuantity - stock.allocatedQuantity;
      if (available < item.quantity) {
        errors.push({ sku: item.sku, reason: `Insufficient stock: ${available} available, ${item.quantity} requested` });
        continue;
      }

      // Create reservation
      const reservation: InventoryReservationEntity = {
        id: `res-${Date.now()}`,
        reservationCode,
        orderId: request.orderId,
        sku: item.sku,
        warehouseId,
        quantity: item.quantity,
        isCommitted: false,
        isReleased: false,
        expiresAt: request.expiresAt || new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours default
        createdAt: new Date(),
        updatedAt: new Date()
      };

      this.reservations.set(reservation.id, reservation);

      // Update stock
      stock.reservedQuantity += item.quantity;
      stock.version++;
      this.stock.set(key, stock);

      reservedItems.push({
        sku: item.sku,
        quantity: item.quantity,
        warehouseId
      });
    }

    return {
      success: errors.length === 0,
      reservationCode: errors.length === 0 ? reservationCode : undefined,
      errors,
      reservedItems
    };
  }

  private findBestWarehouse(sku: string, quantity: number): string {
    // Simple logic: find warehouse with most available stock
    let bestWarehouse = '';
    let maxAvailable = -1;

    for (const [key, stock] of this.stock.entries()) {
      if (key.startsWith(sku)) {
        const available = stock.onHandQuantity - stock.reservedQuantity - stock.allocatedQuantity;
        if (available >= quantity && available > maxAvailable) {
          maxAvailable = available;
          bestWarehouse = stock.warehouseId;
        }
      }
    }

    return bestWarehouse || this.warehouses.keys().next().value || '';
  }

  public async commitReservation(reservationCode: string): Promise<boolean> {
    for (const reservation of this.reservations.values()) {
      if (reservation.reservationCode === reservationCode && !reservation.isReleased) {
        reservation.isCommitted = true;
        reservation.isReleased = true;

        const key = `${reservation.sku}-${reservation.warehouseId}`;
        const stock = this.stock.get(key);
        if (stock) {
          stock.reservedQuantity -= reservation.quantity;
          stock.allocatedQuantity += reservation.quantity;
          stock.version++;
          this.stock.set(key, stock);
        }

        return true;
      }
    }
    return false;
  }

  public async releaseReservation(reservationCode: string): Promise<boolean> {
    for (const reservation of this.reservations.values()) {
      if (reservation.reservationCode === reservationCode && !reservation.isReleased) {
        reservation.isReleased = true;

        const key = `${reservation.sku}-${reservation.warehouseId}`;
        const stock = this.stock.get(key);
        if (stock) {
          stock.reservedQuantity -= reservation.quantity;
          stock.version++;
          this.stock.set(key, stock);
        }

        return true;
      }
    }
    return false;
  }

  public async adjustStock(sku: string, warehouseId: string, quantity: number, reason: string): Promise<void> {
    const key = `${sku}-${warehouseId}`;
    const stock = this.stock.get(key);

    if (stock) {
      stock.onHandQuantity += quantity;
      stock.version++;
      stock.updatedAt = new Date();
      this.stock.set(key, stock);
    } else {
      // Create new stock record
      const newStock: InventoryStockEntity = {
        id: `stock-${Date.now()}`,
        sku,
        warehouseId,
        onHandQuantity: Math.max(0, quantity),
        reservedQuantity: 0,
        allocatedQuantity: 0,
        safetyStockThreshold: 10,
        reorderQuantity: 25,
        version: 1,
        createdAt: new Date(),
        updatedAt: new Date()
      };
      this.stock.set(key, newStock);
    }
  }
}
""")

    # Generate payment service logic
    write_file("services/payment-service/src/domain/payment-processor.ts", """import { PaymentTransactionEntity, Money } from '@novacommerce/core-types';

export interface PaymentRequest {
  orderId: string;
  userId: string;
  amount: Money;
  methodType: 'CREDIT_CARD' | 'DEBIT_CARD' | 'BANK_TRANSFER' | 'PAYPAL' | 'APPLE_PAY' | 'GOOGLE_PAY' | 'STORE_CREDIT';
  paymentDetails: {
    cardNumber?: string;
    cardExpiry?: string;
    cardCvv?: string;
    bankAccountNumber?: string;
    routingNumber?: string;
    paypalEmail?: string;
    applePayToken?: string;
    googlePayToken?: string;
    storeCreditId?: string;
  };
  idempotencyKey: string;
}

export interface PaymentResult {
  success: boolean;
  transactionId?: string;
  providerTransactionId?: string;
  failureReason?: string;
  processedAt: Date;
}

export interface RefundRequest {
  transactionId: string;
  amount?: Money;
  reason: string;
  idempotencyKey: string;
}

export interface RefundResult {
  success: boolean;
  refundTransactionId?: string;
  providerRefundId?: string;
  failureReason?: string;
  processedAt: Date;
}

export class PaymentProcessor {
  private transactions: Map<string, PaymentTransactionEntity> = new Map();

  public async processPayment(request: PaymentRequest): Promise<PaymentResult> {
    // Check idempotency
    const existing = this.findTransactionByIdempotencyKey(request.idempotencyKey);
    if (existing) {
      return {
        success: existing.status === 'COMPLETED',
        transactionId: existing.transactionReference,
        providerTransactionId: existing.providerTransactionId,
        failureReason: existing.failureReason || undefined,
        processedAt: existing.createdAt
      };
    }

    // Process payment based on method type
    let result: PaymentResult;
    switch (request.methodType) {
      case 'CREDIT_CARD':
      case 'DEBIT_CARD':
        result = await this.processCardPayment(request);
        break;
      case 'PAYPAL':
        result = await this.processPayPalPayment(request);
        break;
      case 'APPLE_PAY':
        result = await this.processApplePayPayment(request);
        break;
      case 'GOOGLE_PAY':
        result = await this.processGooglePayPayment(request);
        break;
      case 'STORE_CREDIT':
        result = await this.processStoreCreditPayment(request);
        break;
      default:
        result = {
          success: false,
          failureReason: 'Unsupported payment method',
          processedAt: new Date()
        };
    }

    // Create transaction record
    const transaction: PaymentTransactionEntity = {
      id: `txn-${Date.now()}`,
      transactionReference: result.transactionId || `TXN-${Date.now()}`,
      orderId: request.orderId,
      userId: request.userId,
      amount: request.amount,
      status: result.success ? 'COMPLETED' : 'FAILED',
      methodType: request.methodType,
      provider: this.getProviderForMethod(request.methodType),
      providerTransactionId: result.providerTransactionId,
      failureReason: result.failureReason,
      idempotencyKey: request.idempotencyKey,
      metadata: {
        paymentDetails: this.sanitizePaymentDetails(request.paymentDetails)
      },
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.transactions.set(transaction.id, transaction);

    return result;
  }

  private async processCardPayment(request: PaymentRequest): Promise<PaymentResult> {
    // Simulate card payment processing
    const isValidCard = this.validateCardDetails(request.paymentDetails);

    if (!isValidCard) {
      return {
        success: false,
        failureReason: 'Invalid card details',
        processedAt: new Date()
      };
    }

    // Simulate processing delay
    await this.simulateProcessingDelay(500);

    return {
      success: true,
      transactionId: `CARD-${Date.now()}`,
      providerTransactionId: `STRIPE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processPayPalPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.paypalEmail) {
      return {
        success: false,
        failureReason: 'PayPal email required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(800);

    return {
      success: true,
      transactionId: `PAYPAL-${Date.now()}`,
      providerTransactionId: `PAYPAL-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processApplePayPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.applePayToken) {
      return {
        success: false,
        failureReason: 'Apple Pay token required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(400);

    return {
      success: true,
      transactionId: `APPLE-${Date.now()}`,
      providerTransactionId: `APPLE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processGooglePayPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.googlePayToken) {
      return {
        success: false,
        failureReason: 'Google Pay token required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(450);

    return {
      success: true,
      transactionId: `GOOGLE-${Date.now()}`,
      providerTransactionId: `GOOGLE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  private async processStoreCreditPayment(request: PaymentRequest): Promise<PaymentResult> {
    if (!request.paymentDetails.storeCreditId) {
      return {
        success: false,
        failureReason: 'Store credit ID required',
        processedAt: new Date()
      };
    }

    await this.simulateProcessingDelay(200);

    return {
      success: true,
      transactionId: `CREDIT-${Date.now()}`,
      providerTransactionId: `INTERNAL-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      processedAt: new Date()
    };
  }

  public async processRefund(request: RefundRequest): Promise<RefundResult> {
    const transaction = this.transactions.get(request.transactionId);
    if (!transaction) {
      return {
        success: false,
        failureReason: 'Transaction not found',
        processedAt: new Date()
      };
    }

    if (transaction.status !== 'COMPLETED') {
      return {
        success: false,
        failureReason: 'Cannot refund non-completed transaction',
        processedAt: new Date()
      };
    }

    // Check idempotency
    const existing = this.findTransactionByIdempotencyKey(request.idempotencyKey);
    if (existing) {
      return {
        success: existing.status === 'REFUNDED',
        refundTransactionId: existing.transactionReference,
        providerRefundId: existing.providerTransactionId,
        failureReason: existing.failureReason || undefined,
        processedAt: existing.createdAt
      };
    }

    await this.simulateProcessingDelay(1000);

    const refundTransactionId = `REFUND-${Date.now()}`;
    const providerRefundId = `${transaction.provider}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;

    // Create refund transaction record
    const refundTransaction: PaymentTransactionEntity = {
      id: `txn-${Date.now()}`,
      transactionReference: refundTransactionId,
      orderId: transaction.orderId,
      userId: transaction.userId,
      amount: request.amount || transaction.amount,
      status: 'REFUNDED',
      methodType: transaction.methodType,
      provider: transaction.provider,
      providerTransactionId: providerRefundId,
      idempotencyKey: request.idempotencyKey,
      metadata: {
        originalTransactionId: transaction.transactionReference,
        refundReason: request.reason
      },
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.transactions.set(refundTransaction.id, refundTransaction);

    return {
      success: true,
      refundTransactionId,
      providerRefundId,
      processedAt: new Date()
    };
  }

  private validateCardDetails(details: any): boolean {
    // Basic validation - in production, this would use proper card validation
    const cardNumber = details.cardNumber?.replace(/\s+/g, '');
    return !!(cardNumber && cardNumber.length >= 13 && cardNumber.length <= 19);
  }

  private sanitizePaymentDetails(details: any): any {
    // Remove sensitive data from payment details
    const sanitized = { ...details };
    if (sanitized.cardNumber) {
      sanitized.cardNumber = this.maskCardNumber(sanitized.cardNumber);
    }
    if (sanitized.cardCvv) {
      delete sanitized.cardCvv;
    }
    return sanitized;
  }

  private maskCardNumber(cardNumber: string): string {
    const cleaned = cardNumber.replace(/\s/g, '');
    if (cleaned.length <= 4) return '****';
    return '****' + cleaned.slice(-4);
  }

  private getProviderForMethod(methodType: string): 'STRIPE' | 'PAYPAL' | 'ADYEN' | 'MOCK' | 'INTERNAL_LEDGER' {
    switch (methodType) {
      case 'CREDIT_CARD':
      case 'DEBIT_CARD':
      case 'APPLE_PAY':
      case 'GOOGLE_PAY':
        return 'STRIPE';
      case 'PAYPAL':
        return 'PAYPAL';
      case 'STORE_CREDIT':
        return 'INTERNAL_LEDGER';
      default:
        return 'MOCK';
    }
  }

  private findTransactionByIdempotencyKey(key: string): PaymentTransactionEntity | undefined {
    return Array.from(this.transactions.values()).find(t => t.idempotencyKey === key);
  }

  private simulateProcessingDelay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  public async getTransaction(transactionId: string): Promise<PaymentTransactionEntity | null> {
    return this.transactions.get(transactionId) || null;
  }

  public async getTransactionsByOrder(orderId: string): Promise<PaymentTransactionEntity[]> {
    return Array.from(this.transactions.values()).filter(t => t.orderId === orderId);
  }

  public async getTransactionsByUser(userId: string): Promise<PaymentTransactionEntity[]> {
    return Array.from(this.transactions.values()).filter(t => t.userId === userId);
  }
}
""")

    # Generate shipping service logic
    write_file("services/shipping-service/src/domain/shipping-manager.ts", """import { ShipmentEntity, AddressEntity, Dimensions3D } from '@novacommerce/core-types';

export interface ShippingRateRequest {
  originAddress: AddressEntity;
  destinationAddress: AddressEntity;
  items: {
    weightGrams: number;
    dimensions: Dimensions3D;
    quantity: number;
    valueCents: number;
  }[];
  serviceLevel?: string;
}

export interface ShippingRate {
  carrier: 'FEDEX' | 'UPS' | 'DHL' | 'USPS' | 'INTERNAL_FLEET';
  serviceLevel: string;
  serviceName: string;
  estimatedDays: number;
  rateCents: number;
  currency: string;
}

export interface ShipmentCreationRequest {
  orderId: string;
  carrier: 'FEDEX' | 'UPS' | 'DHL' | 'USPS' | 'INTERNAL_FLEET';
  serviceLevel: string;
  originWarehouseId: string;
  destinationAddress: AddressEntity;
  items: {
    sku: string;
    quantity: number;
    weightGrams: number;
    dimensions: Dimensions3D;
  }[];
}

export class ShippingManager {
  private shipments: Map<string, ShipmentEntity> = new Map();

  public async getShippingRates(request: ShippingRateRequest): Promise<ShippingRate[]> {
    const totalWeight = request.items.reduce((sum, item) => sum + (item.weightGrams * item.quantity), 0);
    const totalValue = request.items.reduce((sum, item) => sum + (item.valueCents * item.quantity), 0);

    // Calculate rates for each carrier
    const rates: ShippingRate[] = [];

    // FedEx rates
    rates.push({
      carrier: 'FEDEX',
      serviceLevel: 'FEDEX_GROUND',
      serviceName: 'FedEx Ground',
      estimatedDays: this.calculateEstimatedDays(request.originAddress, request.destinationAddress, 'ground'),
      rateCents: this.calculateRate('FEDEX', totalWeight, totalValue, 'ground'),
      currency: 'USD'
    });

    rates.push({
      carrier: 'FEDEX',
      serviceLevel: 'FEDEX_EXPRESS',
      serviceName: 'FedEx Express',
      estimatedDays: this.calculateEstimatedDays(request.originAddress, request.destinationAddress, 'express'),
      rateCents: this.calculateRate('FEDEX', totalWeight, totalValue, 'express'),
      currency: 'USD'
    });

    // UPS rates
    rates.push({
      carrier: 'UPS',
      serviceLevel: 'UPS_GROUND',
      serviceName: 'UPS Ground',
      estimatedDays: this.calculateEstimatedDays(request.originAddress, request.destinationAddress, 'ground'),
      rateCents: this.calculateRate('UPS', totalWeight, totalValue, 'ground'),
      currency: 'USD'
    });

    rates.push({
      carrier: 'UPS',
      serviceLevel: 'UPS_NEXT_DAY',
      serviceName: 'UPS Next Day Air',
      estimatedDays: 1,
      rateCents: this.calculateRate('UPS', totalWeight, totalValue, 'next_day'),
      currency: 'USD'
    });

    // USPS rates
    rates.push({
      carrier: 'USPS',
      serviceLevel: 'USPS_PRIORITY',
      serviceName: 'USPS Priority Mail',
      estimatedDays: this.calculateEstimatedDays(request.originAddress, request.destinationAddress, 'priority'),
      rateCents: this.calculateRate('USPS', totalWeight, totalValue, 'priority'),
      currency: 'USD'
    });

    // Sort by rate
    rates.sort((a, b) => a.rateCents - b.rateCents);

    return rates;
  }

  private calculateEstimatedDays(origin: AddressEntity, destination: AddressEntity, serviceType: string): number {
    // Simple distance-based estimation
    const isSameState = origin.stateOrProvince === destination.stateOrProvince;
    const isSameRegion = this.isSameRegion(origin.stateOrProvince, destination.stateOrProvince);

    switch (serviceType) {
      case 'ground':
        if (isSameState) return 1;
        if (isSameRegion) return 2;
        return 5;
      case 'express':
        if (isSameState) return 1;
        if (isSameRegion) return 2;
        return 3;
      case 'priority':
        if (isSameState) return 1;
        if (isSameRegion) return 2;
        return 3;
      case 'next_day':
        return 1;
      default:
        return 5;
    }
  }

  private isSameRegion(state1: string, state2: string): boolean {
    const regions: Record<string, string[]> = {
      'west': ['CA', 'OR', 'WA', 'NV', 'AZ'],
      'midwest': ['IL', 'IN', 'OH', 'MI', 'WI'],
      'east': ['NY', 'NJ', 'PA', 'MA', 'CT'],
      'south': ['TX', 'FL', 'GA', 'NC', 'VA']
    };

    for (const region of Object.values(regions)) {
      if (region.includes(state1) && region.includes(state2)) {
        return true;
      }
    }
    return false;
  }

  private calculateRate(carrier: string, weightGrams: number, valueCents: number, serviceType: string): number {
    // Simplified rate calculation
    const weightLbs = weightGrams / 453.592;
    const baseRate = this.getBaseRate(carrier, serviceType);
    const weightRate = weightLbs * this.getWeightRate(carrier, serviceType);
    const valueRate = (valueCents / 100) * 0.01; // 1% insurance

    return Math.round(baseRate + weightRate + valueRate);
  }

  private getBaseRate(carrier: string, serviceType: string): number {
    const baseRates: Record<string, Record<string, number>> = {
      'FEDEX': { ground: 800, express: 2500 },
      'UPS': { ground: 750, next_day: 3500 },
      'USPS': { priority: 700 }
    };

    return baseRates[carrier]?.[serviceType] || 1000;
  }

  private getWeightRate(carrier: string, serviceType: string): number {
    const weightRates: Record<string, Record<string, number>> = {
      'FEDEX': { ground: 100, express: 200 },
      'UPS': { ground: 95, next_day: 300 },
      'USPS': { priority: 80 }
    };

    return weightRates[carrier]?.[serviceType] || 100;
  }

  public async createShipment(request: ShipmentCreationRequest): Promise<ShipmentEntity> {
    const totalWeight = request.items.reduce((sum, item) => sum + (item.weightGrams * item.quantity), 0);
    const totalDimensions = this.calculateTotalDimensions(request.items);

    const shipment: ShipmentEntity = {
      id: `shipment-${Date.now()}`,
      shipmentNumber: `SHP-${Date.now()}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`,
      orderId: request.orderId,
      status: 'PENDING',
      carrier: request.carrier,
      serviceLevel: request.serviceLevel,
      trackingNumber: this.generateTrackingNumber(request.carrier),
      trackingUrl: this.generateTrackingUrl(request.carrier, ''),
      originWarehouseId: request.originWarehouseId,
      destinationAddress: request.destinationAddress,
      weightGrams: totalWeight,
      dimensionsMm: totalDimensions,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.shipments.set(shipment.id, shipment);

    return shipment;
  }

  private calculateTotalDimensions(items: { dimensions: Dimensions3D; quantity: number }[]): Dimensions3D {
    // Simplified dimension calculation
    return items.reduce((acc, item) => ({
      length: Math.max(acc.length, item.dimensions.length),
      width: Math.max(acc.width, item.dimensions.width),
      height: acc.height + (item.dimensions.height * item.quantity)
    }), { length: 0, width: 0, height: 0 });
  }

  private generateTrackingNumber(carrier: string): string {
    const prefixes: Record<string, string> = {
      'FEDEX': '1Z',
      'UPS': '1Z',
      'DHL': 'JD',
      'USPS': '94',
      'INTERNAL_FLEET': 'INT'
    };

    const prefix = prefixes[carrier] || 'TRK';
    const random = Math.random().toString(36).substr(2, 12).toUpperCase();
    return `${prefix}${random}`;
  }

  private generateTrackingUrl(carrier: string, trackingNumber: string): string {
    const urls: Record<string, string> = {
      'FEDEX': `https://www.fedex.com/fedextrack/?trknbr=${trackingNumber}`,
      'UPS': `https://www.ups.com/track?loc=en_US&tracknum=${trackingNumber}`,
      'DHL': `https://www.dhl.com/us-en/home/tracking.html?tracking-id=${trackingNumber}`,
      'USPS': `https://tools.usps.com/go/TrackConfirmAction?tLabels=${trackingNumber}`,
      'INTERNAL_FLEET': `https://fleet.novacommerce.io/track/${trackingNumber}`
    };

    return urls[carrier] || '';
  }

  public async updateShipmentStatus(shipmentId: string, status: 'PENDING' | 'PROCESSING' | 'DISPATCHED' | 'IN_TRANSIT' | 'OUT_FOR_DELIVERY' | 'DELIVERED' | 'FAILED' | 'RETURNED'): Promise<ShipmentEntity> {
    const shipment = this.shipments.get(shipmentId);
    if (!shipment) {
      throw new Error(`Shipment not found: ${shipmentId}`);
    }

    shipment.status = status;
    shipment.updatedAt = new Date();

    if (status === 'DISPATCHED') {
      shipment.dispatchedAt = new Date();
    } else if (status === 'DELIVERED') {
      shipment.deliveredAt = new Date();
    }

    this.shipments.set(shipmentId, shipment);

    return shipment;
  }

  public async getShipment(shipmentId: string): Promise<ShipmentEntity | null> {
    return this.shipments.get(shipmentId) || null;
  }

  public async getShipmentsByOrder(orderId: string): Promise<ShipmentEntity[]> {
    return Array.from(this.shipments.values()).filter(s => s.orderId === orderId);
  }
}
""")

    # Generate user service logic
    write_file("services/user-service/src/domain/user-manager.ts", """import { UserEntity, UserProfileEntity, AddressEntity, OrganizationEntity, OrganizationMemberEntity } from '@novacommerce/core-types';

export interface CreateUserRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phoneNumber?: string;
  organizationId?: string;
}

export interface UpdateUserRequest {
  firstName?: string;
  lastName?: string;
  phoneNumber?: string;
  avatarUrl?: string;
  timezone?: string;
  locale?: string;
}

export class UserManager {
  private users: Map<string, UserEntity> = new Map();
  private profiles: Map<string, UserProfileEntity> = new Map();
  private addresses: Map<string, AddressEntity> = new Map();
  private organizations: Map<string, OrganizationEntity> = new Map();
  private organizationMembers: Map<string, OrganizationMemberEntity> = new Map();

  public async createUser(request: CreateUserRequest): Promise<UserEntity> {
    // Check if user already exists
    const existing = Array.from(this.users.values()).find(u => u.email === request.email);
    if (existing) {
      throw new Error('User with this email already exists');
    }

    const passwordHash = await this.hashPassword(request.password);

    const user: UserEntity = {
      id: `user-${Date.now()}`,
      email: request.email,
      passwordHash,
      role: 'CUSTOMER',
      status: 'ACTIVE',
      kycStatus: 'NOT_VERIFIED',
      organizationId: request.organizationId || null,
      isMfaEnabled: false,
      failedLoginAttempts: 0,
      passwordChangedAt: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.users.set(user.id, user);

    // Create user profile
    const profile: UserProfileEntity = {
      id: `profile-${Date.now()}`,
      userId: user.id,
      firstName: request.firstName,
      lastName: request.lastName,
      phoneNumber: request.phoneNumber || null,
      avatarUrl: null,
      timezone: 'UTC',
      locale: 'en-US',
      preferences: {
        marketingEmails: true,
        orderSmsNotifications: true,
        twoFactorRequiredForOrders: false,
        preferredCurrency: 'USD',
        theme: 'system'
      },
      metadata: {},
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.profiles.set(profile.id, profile);

    return user;
  }

  public async getUserById(userId: string): Promise<UserEntity | null> {
    return this.users.get(userId) || null;
  }

  public async getUserByEmail(email: string): Promise<UserEntity | null> {
    return Array.from(this.users.values()).find(u => u.email === email) || null;
  }

  public async getUserProfile(userId: string): Promise<UserProfileEntity | null> {
    return Array.from(this.profiles.values()).find(p => p.userId === userId) || null;
  }

  public async updateUser(userId: string, request: UpdateUserRequest): Promise<UserProfileEntity> {
    const profile = Array.from(this.profiles.values()).find(p => p.userId === userId);
    if (!profile) {
      throw new Error('User profile not found');
    }

    if (request.firstName !== undefined) profile.firstName = request.firstName;
    if (request.lastName !== undefined) profile.lastName = request.lastName;
    if (request.phoneNumber !== undefined) profile.phoneNumber = request.phoneNumber;
    if (request.avatarUrl !== undefined) profile.avatarUrl = request.avatarUrl;
    if (request.timezone !== undefined) profile.timezone = request.timezone;
    if (request.locale !== undefined) profile.locale = request.locale;

    profile.updatedAt = new Date();
    this.profiles.set(profile.id, profile);

    return profile;
  }

  public async addAddress(userId: string, address: Omit<AddressEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<AddressEntity> {
    const newAddress: AddressEntity = {
      ...address,
      id: `addr-${Date.now()}`,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.addresses.set(newAddress.id, newAddress);

    return newAddress;
  }

  public async getUserAddresses(userId: string): Promise<AddressEntity[]> {
    return Array.from(this.addresses.values()).filter(a => a.userId === userId);
  }

  public async updateAddress(addressId: string, updates: Partial<AddressEntity>): Promise<AddressEntity> {
    const address = this.addresses.get(addressId);
    if (!address) {
      throw new Error('Address not found');
    }

    Object.assign(address, updates);
    address.updatedAt = new Date();
    this.addresses.set(addressId, address);

    return address;
  }

  public async deleteAddress(addressId: string): Promise<boolean> {
    return this.addresses.delete(addressId);
  }

  public async createOrganization(name: string, billingEmail: string, userId: string): Promise<OrganizationEntity> {
    const slug = this.generateSlug(name);

    const organization: OrganizationEntity = {
      id: `org-${Date.now()}`,
      name,
      slug,
      billingEmail,
      tier: 'FREE',
      maxSeats: 5,
      isActive: true,
      settings: {},
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.organizations.set(organization.id, organization);

    // Add creator as owner
    const member: OrganizationMemberEntity = {
      id: `member-${Date.now()}`,
      organizationId: organization.id,
      userId,
      role: 'OWNER',
      joinedAt: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.organizationMembers.set(member.id, member);

    // Update user with organization
    const user = this.users.get(userId);
    if (user) {
      user.organizationId = organization.id;
      user.updatedAt = new Date();
      this.users.set(userId, user);
    }

    return organization;
  }

  public async getOrganizationById(orgId: string): Promise<OrganizationEntity | null> {
    return this.organizations.get(orgId) || null;
  }

  public async getOrganizationBySlug(slug: string): Promise<OrganizationEntity | null> {
    return Array.from(this.organizations.values()).find(o => o.slug === slug) || null;
  }

  public async addOrganizationMember(orgId: string, userId: string, role: 'ADMIN' | 'MEMBER' | 'BILLING_MANAGER' | 'READ_ONLY'): Promise<OrganizationMemberEntity> {
    const member: OrganizationMemberEntity = {
      id: `member-${Date.now()}`,
      organizationId: orgId,
      userId,
      role,
      joinedAt: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.organizationMembers.set(member.id, member);

    return member;
  }

  public async getOrganizationMembers(orgId: string): Promise<OrganizationMemberEntity[]> {
    return Array.from(this.organizationMembers.values()).filter(m => m.organizationId === orgId);
  }

  public async updateOrganizationMember(memberId: string, role: 'ADMIN' | 'MEMBER' | 'BILLING_MANAGER' | 'READ_ONLY'): Promise<OrganizationMemberEntity> {
    const member = this.organizationMembers.get(memberId);
    if (!member) {
      throw new Error('Organization member not found');
    }

    member.role = role;
    member.updatedAt = new Date();
    this.organizationMembers.set(memberId, member);

    return member;
  }

  public async removeOrganizationMember(memberId: string): Promise<boolean> {
    return this.organizationMembers.delete(memberId);
  }

  private async hashPassword(password: string): Promise<string> {
    // In production, use proper password hashing (bcrypt, argon2, etc.)
    // This is a placeholder implementation
    const hash = password.split('').reduce((acc, char) => {
      return ((acc << 5) - acc) + char.charCodeAt(0);
    }, 0);
    return `HASH_${Math.abs(hash).toString(16)}`;
  }

  private generateSlug(name: string): string {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '')
      .substring(0, 50);
  }

  public async verifyPassword(email: string, password: string): Promise<UserEntity | null> {
    const user = await this.getUserByEmail(email);
    if (!user) {
      return null;
    }

    const passwordHash = await this.hashPassword(password);
    if (user.passwordHash !== passwordHash) {
      user.failedLoginAttempts++;
      if (user.failedLoginAttempts >= 5) {
        user.lockedUntil = new Date(Date.now() + 15 * 60 * 1000); // Lock for 15 minutes
      }
      user.updatedAt = new Date();
      this.users.set(user.id, user);
      return null;
    }

    // Reset failed attempts on successful login
    user.failedLoginAttempts = 0;
    user.lastLoginAt = new Date();
    user.updatedAt = new Date();
    this.users.set(user.id, user);

    return user;
  }

  public async changePassword(userId: string, oldPassword: string, newPassword: string): Promise<boolean> {
    const user = this.users.get(userId);
    if (!user) {
      return false;
    }

    const oldPasswordHash = await this.hashPassword(oldPassword);
    if (user.passwordHash !== oldPasswordHash) {
      return false;
    }

    user.passwordHash = await this.hashPassword(newPassword);
    user.passwordChangedAt = new Date();
    user.updatedAt = new Date();
    this.users.set(userId, user);

    return true;
  }
}
""")

    print("Generated extended production code across multiple services.")

if __name__ == "__main__":
    generate_extended_production_code()
