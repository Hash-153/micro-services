import { WarehouseEntity } from '@novacommerce/core-types';

export interface GeoCoordinate {
  latitude: number;
  longitude: number;
}

export class HaversineWarehouseRouter {
  public static calculateDistanceKm(coordA: GeoCoordinate, coordB: GeoCoordinate): number {
    const R = 6371; // Earth radius in kilometers
    const dLat = this.toRadians(coordB.latitude - coordA.latitude);
    const dLon = this.toRadians(coordB.longitude - coordA.longitude);

    const lat1 = this.toRadians(coordA.latitude);
    const lat2 = this.toRadians(coordB.latitude);

    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * c * 10) / 10;
  }

  public static findNearestWarehouses(
    destination: GeoCoordinate,
    warehouses: WarehouseEntity[],
    limit: number = 3
  ): { warehouse: WarehouseEntity; distanceKm: number }[] {
    return warehouses
      .filter(w => w.isActive)
      .map(warehouse => ({
        warehouse,
        distanceKm: this.calculateDistanceKm(destination, {
          latitude: warehouse.latitude,
          longitude: warehouse.longitude
        })
      }))
      .sort((a, b) => a.distanceKm - b.distanceKm)
      .slice(0, limit);
  }

  private static toRadians(degrees: number): number {
    return (degrees * Math.PI) / 180;
  }
}
