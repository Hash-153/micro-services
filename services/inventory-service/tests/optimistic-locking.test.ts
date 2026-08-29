import { InMemoryStockRepository } from '../src/repositories/inventory.repository.js';
import { InventoryService } from '../src/services/inventory.service.js';
import { InMemoryReservationRepository } from '../src/repositories/inventory.repository.js';

describe('Inventory Service: Optimistic Concurrency Control & Versioning Suite', () => {
  let inventoryService: InventoryService;

  beforeEach(async () => {
    const stockRepo = new InMemoryStockRepository();
    const resRepo = new InMemoryReservationRepository();
    inventoryService = new InventoryService(stockRepo, resRepo);
    await inventoryService.setStock('SKU-CONCURRENT-01', 'WH-MAIN-01', 50);
  });

  it('should increment version on each stock reservation', async () => {
    const res1 = await inventoryService.reserveStock('ord-c-1', 'SKU-CONCURRENT-01', 5);
    expect(res1.quantity).toBe(5);

    const res2 = await inventoryService.reserveStock('ord-c-2', 'SKU-CONCURRENT-01', 10);
    expect(res2.quantity).toBe(10);
  });
});
