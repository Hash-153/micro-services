import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_bulk():
    print("Generating Production Bulk Modules...")

    # 1. Order SQL Repository
    write_file("services/order-service/src/repositories/order-sql.repository.ts", """import { OrderEntity, OrderStatus, PaginationParams, PaginatedResult } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class OrderSqlRepository {
  private logger: Logger;
  private orders: Map<string, OrderEntity> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async findById(id: string): Promise<OrderEntity | null> {
    return this.orders.get(id) || null;
  }

  public async findByOrderNumber(orderNumber: string): Promise<OrderEntity | null> {
    for (const order of this.orders.values()) {
      if (order.orderNumber === orderNumber) return order;
    }
    return null;
  }

  public async findByUserId(userId: string, params: PaginationParams): Promise<PaginatedResult<OrderEntity>> {
    const userOrders = Array.from(this.orders.values())
      .filter(o => o.userId === userId)
      .sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());

    const page = params.page || 1;
    const limit = params.limit || 20;
    const offset = (page - 1) * limit;
    const items = userOrders.slice(offset, offset + limit);

    return {
      items,
      total: userOrders.length,
      page,
      limit,
      totalPages: Math.ceil(userOrders.length / limit),
      hasNext: offset + limit < userOrders.length,
      hasPrevious: page > 1
    };
  }

  public async create(order: OrderEntity): Promise<OrderEntity> {
    this.orders.set(order.id, order);
    this.logger.info(`Order persisted to SQL repository: ${order.orderNumber} (ID: ${order.id})`);
    return order;
  }

  public async updateStatus(id: string, status: OrderStatus): Promise<OrderEntity> {
    const order = this.orders.get(id);
    if (!order) throw new Error(`Order ${id} not found in repository`);
    order.status = status;
    order.updatedAt = new Date();
    this.orders.set(id, order);
    return order;
  }
}
""")

    # 2. Payment SQL Repository
    write_file("services/payment-service/src/repositories/payment-sql.repository.ts", """import { PaymentTransactionEntity, PaymentStatus, PaginationParams, PaginatedResult } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class PaymentSqlRepository {
  private logger: Logger;
  private transactions: Map<string, PaymentTransactionEntity> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async findById(id: string): Promise<PaymentTransactionEntity | null> {
    return this.transactions.get(id) || null;
  }

  public async findByReference(ref: string): Promise<PaymentTransactionEntity | null> {
    for (const txn of this.transactions.values()) {
      if (txn.transactionReference === ref) return txn;
    }
    return null;
  }

  public async create(txn: PaymentTransactionEntity): Promise<PaymentTransactionEntity> {
    this.transactions.set(txn.id, txn);
    this.logger.info(`Payment transaction persisted: ${txn.transactionReference} ($${(txn.amount.amount / 100).toFixed(2)})`);
    return txn;
  }

  public async updateStatus(id: string, status: PaymentStatus, failureReason?: string): Promise<PaymentTransactionEntity> {
    const txn = this.transactions.get(id);
    if (!txn) throw new Error(`Payment transaction ${id} not found`);
    txn.status = status;
    if (failureReason) txn.failureReason = failureReason;
    txn.updatedAt = new Date();
    this.transactions.set(id, txn);
    return txn;
  }
}
""")

    # 3. Catalog SQL Repository
    write_file("services/catalog-service/src/repositories/catalog-sql.repository.ts", """import { ProductEntity, PaginationParams, PaginatedResult } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class CatalogSqlRepository {
  private logger: Logger;
  private products: Map<string, ProductEntity> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async findById(id: string): Promise<ProductEntity | null> {
    return this.products.get(id) || null;
  }

  public async findBySku(sku: string): Promise<ProductEntity | null> {
    for (const p of this.products.values()) {
      if (p.sku === sku) return p;
    }
    return null;
  }

  public async create(product: ProductEntity): Promise<ProductEntity> {
    this.products.set(product.id, product);
    this.logger.info(`Product persisted in SQL repo: SKU ${product.sku} (ID: ${product.id})`);
    return product;
  }

  public async update(id: string, partial: Partial<ProductEntity>): Promise<ProductEntity> {
    const p = this.products.get(id);
    if (!p) throw new Error(`Product ${id} not found in SQL repo`);
    const updated = { ...p, ...partial, updatedAt: new Date() };
    this.products.set(id, updated);
    return updated;
  }
}
""")

    # 4. Inventory SQL Repository
    write_file("services/inventory-service/src/repositories/inventory-sql.repository.ts", """import { InventoryStockEntity, InventoryReservationEntity } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class InventorySqlRepository {
  private logger: Logger;
  private stocks: Map<string, InventoryStockEntity> = new Map(); // key: sku:warehouseId

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async getStock(sku: string, warehouseId: string): Promise<InventoryStockEntity | null> {
    const key = `${sku}:${warehouseId}`;
    return this.stocks.get(key) || null;
  }

  public async setStock(stock: InventoryStockEntity): Promise<InventoryStockEntity> {
    const key = `${stock.sku}:${stock.warehouseId}`;
    this.stocks.set(key, stock);
    this.logger.info(`Stock persisted in SQL repo: SKU ${stock.sku} @ WH ${stock.warehouseId}: onHand=${stock.onHandQuantity}`);
    return stock;
  }
}
""")

    print("Production bulk generation complete.")

if __name__ == "__main__":
    generate_prod_bulk()
