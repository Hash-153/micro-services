export interface EnvironmentalReading {
  sensorId: string;
  zoneId: string;
  temperatureCelsius: number;
  relativeHumidityPercentage: number;
  recordedAt: Date;
}

export class WarehouseTelemetryMonitor {
  private static readonly MAX_TEMP_CELSIUS = 25.0; // Cold storage max 25C
  private static readonly MIN_TEMP_CELSIUS = 2.0;

  public static evaluateReading(reading: EnvironmentalReading): { isAlert: boolean; alertType?: 'TEMP_HIGH' | 'TEMP_LOW' | 'HUMIDITY_HIGH'; message?: string } {
    if (reading.temperatureCelsius > this.MAX_TEMP_CELSIUS) {
      return {
        isAlert: true,
        alertType: 'TEMP_HIGH',
        message: `High temperature alert in zone ${reading.zoneId}: ${reading.temperatureCelsius}°C exceeds max threshold (${this.MAX_TEMP_CELSIUS}°C)`
      };
    }

    if (reading.temperatureCelsius < this.MIN_TEMP_CELSIUS) {
      return {
        isAlert: true,
        alertType: 'TEMP_LOW',
        message: `Low temperature alert in zone ${reading.zoneId}: ${reading.temperatureCelsius}°C below min threshold (${this.MIN_TEMP_CELSIUS}°C)`
      };
    }

    if (reading.relativeHumidityPercentage > 75.0) {
      return {
        isAlert: true,
        alertType: 'HUMIDITY_HIGH',
        message: `High relative humidity in zone ${reading.zoneId}: ${reading.relativeHumidityPercentage}%`
      };
    }

    return { isAlert: false };
  }
}
