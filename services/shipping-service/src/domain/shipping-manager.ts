import { ShipmentEntity, AddressEntity, Dimensions3D } from '@novacommerce/core-types';

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
