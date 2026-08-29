import { InMemoryStockRepository, InMemoryReservationRepository } from '../repositories/inventory.repository.js';
import { InventoryStockEntity, InventoryReservationEntity, InsufficientStockError, NotFoundError } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class InventoryService {
  private readonly stockRepo: InMemoryStockRepository;
  private readonly reservationRepo: InMemoryReservationRepository;
  private readonly eventBus?: IEventBus;

  constructor(stockRepo: InMemoryStockRepository, reservationRepo: InMemoryReservationRepository, eventBus?: IEventBus) {
    this.stockRepo = stockRepo;
    this.reservationRepo = reservationRepo;
    this.eventBus = eventBus;
  }

  public async setStock(sku: string, warehouseId: string, quantity: number): Promise<InventoryStockEntity> {
    let stock = await this.stockRepo.findBySku(sku);
    if (!stock) {
      stock = await this.stockRepo.create({
        id: randomUUID(),
        sku,
        warehouseId,
        onHandQuantity: quantity,
        reservedQuantity: 0,
        allocatedQuantity: 0,
        safetyStockThreshold: 5,
        reorderQuantity: 20,
        version: 1,
        updatedAt: new Date()
      });
    } else {
      stock = await this.stockRepo.update(stock.id, {
        onHandQuantity: quantity,
        version: stock.version + 1
      }) as InventoryStockEntity;
    }
    return stock;
  }

  public async reserveStock(orderId: string, sku: string, quantity: number, correlationId?: string): Promise<InventoryReservationEntity> {
    const stock = await this.stockRepo.findBySku(sku);
    if (!stock) {
      throw new NotFoundError('InventoryStock for SKU', sku);
    }

    const available = stock.onHandQuantity - stock.reservedQuantity;
    if (available < quantity) {
      throw new InsufficientStockError(sku, quantity, available);
    }

    await this.stockRepo.update(stock.id, {
      reservedQuantity: stock.reservedQuantity + quantity,
      version: stock.version + 1
    });

    const reservation = await this.reservationRepo.create({
      id: randomUUID(),
      reservationCode: `RES-${randomUUID().substring(0, 8).toUpperCase()}`,
      orderId,
      sku,
      warehouseId: stock.warehouseId,
      quantity,
      isCommitted: false,
      isReleased: false,
      expiresAt: new Date(Date.now() + 30 * 60 * 1000), // 30 mins
      createdAt: new Date(),
      updatedAt: new Date()
    });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.INVENTORY_RESERVATION_CREATED,
        reservation.id,
        'InventoryReservation',
        reservation,
        'inventory-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return reservation;
  }

  public async releaseReservation(orderId: string, correlationId?: string): Promise<void> {
    const reservations = await this.reservationRepo.findByOrderId(orderId);
    for (const res of reservations) {
      if (!res.isReleased && !res.isCommitted) {
        const stock = await this.stockRepo.findBySku(res.sku);
        if (stock) {
          await this.stockRepo.update(stock.id, {
            reservedQuantity: Math.max(0, stock.reservedQuantity - res.quantity),
            version: stock.version + 1
          });
        }
        await this.reservationRepo.update(res.id, { isReleased: true });

        if (this.eventBus) {
          const event = DomainEventFactory.create(
            EventType.INVENTORY_RESERVATION_RELEASED,
            res.id,
            'InventoryReservation',
            res,
            'inventory-service',
            correlationId
          );
          await this.eventBus.publish(event);
        }
      }
    }
  }
}
