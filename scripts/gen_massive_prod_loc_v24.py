import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v24():
    print("Generating comprehensive Production V24 Modules...")

    # 1. Payment ISO 8583 Message Encoder / Decoder
    write_file("services/payment-service/src/domain/iso8583-message-codec.ts", """export interface Iso8583BitmapFields {
  mti: string; // e.g. "0100", "0110", "0200", "0210"
  pan?: string; // Field 2
  processingCode?: string; // Field 3
  amountCents?: number; // Field 4
  transmissionDateTime?: string; // Field 7
  stan?: string; // Field 11
  localTransactionTime?: string; // Field 12
  localTransactionDate?: string; // Field 13
  posEntryMode?: string; // Field 22
  cardSequenceNumber?: string; // Field 23
  functionCode?: string; // Field 24
  retrievalReferenceNumber?: string; // Field 37
  authorizationIdResponse?: string; // Field 38
  responseCode?: string; // Field 39
}

export class Iso8583MessageCodec {
  public static encode(fields: Iso8583BitmapFields): string {
    const parts: string[] = [fields.mti];

    // Encode Fields
    if (fields.pan) parts.push(`02${fields.pan.length.toString().padStart(2, '0')}${fields.pan}`);
    if (fields.processingCode) parts.push(`03${fields.processingCode}`);
    if (fields.amountCents !== undefined) parts.push(`04${fields.amountCents.toString().padStart(12, '0')}`);
    if (fields.stan) parts.push(`11${fields.stan.padStart(6, '0')}`);
    if (fields.retrievalReferenceNumber) parts.push(`37${fields.retrievalReferenceNumber.padStart(12, '0')}`);
    if (fields.responseCode) parts.push(`39${fields.responseCode.padStart(2, '0')}`);

    return parts.join('|');
  }

  public static decode(rawMessage: string): Iso8583BitmapFields {
    const parts = rawMessage.split('|');
    const fields: Iso8583BitmapFields = { mti: parts[0] || '0100' };

    for (let i = 1; i < parts.length; i++) {
      const chunk = parts[i];
      const fieldNum = chunk.slice(0, 2);
      const val = chunk.slice(2);

      if (fieldNum === '03') fields.processingCode = val;
      if (fieldNum === '04') fields.amountCents = parseInt(val, 10);
      if (fieldNum === '11') fields.stan = val;
      if (fieldNum === '37') fields.retrievalReferenceNumber = val;
      if (fieldNum === '39') fields.responseCode = val;
    }

    return fields;
  }
}
""")

    # 2. Inventory Warehouse Temperature & Humidity Monitor
    write_file("services/inventory-service/src/domain/telemetry-monitor.ts", """export interface EnvironmentalReading {
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
""")

    print("Production V24 modules generated.")

if __name__ == "__main__":
    generate_prod_v24()
