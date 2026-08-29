import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_domain_matrix():
    print("Generating comprehensive Production Domain Matrix...")

    # 1. Product Catalog Attribute Schema Registry
    write_file("services/catalog-service/src/domain/attribute-schema-registry.ts", """import { ProductAttributeSchemaDefinition } from '@novacommerce/core-types';

export class AttributeSchemaRegistry {
  private static readonly SCHEMAS: Map<string, ProductAttributeSchemaDefinition[]> = new Map();

  static {
    // Laptops & Workstations
    this.SCHEMAS.set('cat-laptops', [
      { attributeKey: 'processorModel', label: 'Processor (CPU)', dataType: 'STRING', isRequired: true },
      { attributeKey: 'ramGigabytes', label: 'Memory (RAM GB)', dataType: 'NUMBER', isRequired: true, minValue: 4, maxValue: 256 },
      { attributeKey: 'storageGigabytes', label: 'Storage Capacity (GB)', dataType: 'NUMBER', isRequired: true, minValue: 128, maxValue: 16000 },
      { attributeKey: 'screenSizeInches', label: 'Screen Size (Inches)', dataType: 'NUMBER', isRequired: true, minValue: 11, maxValue: 21 },
      { attributeKey: 'hasDedicatedGpu', label: 'Dedicated Graphics GPU', dataType: 'BOOLEAN', isRequired: false },
      { attributeKey: 'operatingSystem', label: 'Operating System', dataType: 'ENUM', isRequired: true, allowedValues: ['macOS', 'Windows 11 Pro', 'Ubuntu Linux', 'RHEL'] }
    ]);

    // Monitors & Displays
    this.SCHEMAS.set('cat-monitors', [
      { attributeKey: 'resolution', label: 'Display Resolution', dataType: 'ENUM', isRequired: true, allowedValues: ['1080p FHD', '1440p QHD', '4K UHD', '5K2K', '8K'] },
      { attributeKey: 'refreshRateHz', label: 'Refresh Rate (Hz)', dataType: 'NUMBER', isRequired: true, minValue: 60, maxValue: 500 },
      { attributeKey: 'panelType', label: 'Panel Technology', dataType: 'ENUM', isRequired: true, allowedValues: ['IPS', 'OLED', 'Mini-LED', 'VA'] },
      { attributeKey: 'hasUsbCHub', label: 'USB-C Power Delivery Hub', dataType: 'BOOLEAN', isRequired: false }
    ]);

    // Servers & Storage
    this.SCHEMAS.set('cat-rack-servers', [
      { attributeKey: 'rackUnits', label: 'Form Factor (Rack Units)', dataType: 'ENUM', isRequired: true, allowedValues: ['1U', '2U', '4U'] },
      { attributeKey: 'socketCount', label: 'CPU Sockets', dataType: 'NUMBER', isRequired: true, minValue: 1, maxValue: 4 },
      { attributeKey: 'maxMemoryTerabytes', label: 'Max RAM Capacity (TB)', dataType: 'NUMBER', isRequired: true, minValue: 0.25, maxValue: 16 },
      { attributeKey: 'powerSupplyWattage', label: 'Redundant PSU Wattage', dataType: 'NUMBER', isRequired: true, minValue: 500, maxValue: 3200 }
    ]);
  }

  public static getSchemaForCategory(categoryId: string): ProductAttributeSchemaDefinition[] {
    return this.SCHEMAS.get(categoryId) || [];
  }

  public static validateProductAttributes(categoryId: string, attributes: Record<string, any>): { isValid: boolean; errors: string[] } {
    const schema = this.getSchemaForCategory(categoryId);
    const errors: string[] = [];

    for (const field of schema) {
      const val = attributes[field.attributeKey];

      if (field.isRequired && (val === undefined || val === null || val === '')) {
        errors.push(`Attribute '${field.label}' (${field.attributeKey}) is required.`);
        continue;
      }

      if (val !== undefined && val !== null) {
        if (field.dataType === 'NUMBER') {
          const num = Number(val);
          if (isNaN(num)) {
            errors.push(`Attribute '${field.label}' must be a numeric value.`);
          } else {
            if (field.minValue !== undefined && num < field.minValue) {
              errors.push(`Attribute '${field.label}' cannot be less than ${field.minValue}.`);
            }
            if (field.maxValue !== undefined && num > field.maxValue) {
              errors.push(`Attribute '${field.label}' cannot exceed ${field.maxValue}.`);
            }
          }
        } else if (field.dataType === 'ENUM') {
          if (field.allowedValues && !field.allowedValues.includes(String(val))) {
            errors.push(`Attribute '${field.label}' must be one of: ${field.allowedValues.join(', ')}.`);
          }
        } else if (field.dataType === 'BOOLEAN') {
          if (typeof val !== 'boolean') {
            errors.push(`Attribute '${field.label}' must be a boolean.`);
          }
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}
""")

    # 2. Inventory Safety Stock Formulas
    write_file("services/inventory-service/src/domain/safety-stock-matrix.ts", """export interface StockDemandParameters {
  sku: string;
  dailyDemandMean: number;
  dailyDemandVariance: number;
  leadTimeDaysMean: number;
  leadTimeDaysVariance: number;
  targetServiceLevelPercent: number; // e.g. 95 or 99
}

export class SafetyStockMatrixCalculator {
  private static readonly Z_SCORE_TABLE: Record<number, number> = {
    90: 1.282,
    95: 1.645,
    98: 2.054,
    99: 2.326,
    99.9: 3.090
  };

  public static calculateComprehensiveSafetyStock(params: StockDemandParameters): {
    safetyStockUnits: number;
    reorderPointUnits: number;
    serviceLevelZScore: number;
    combinedStandardDeviation: number;
  } {
    const zScore = this.Z_SCORE_TABLE[params.targetServiceLevelPercent] || 1.645;

    // Combined variance formula: Var(Demand during Lead Time) = L * Var(D) + D^2 * Var(L)
    const demandVariance = params.dailyDemandVariance;
    const leadTimeVariance = params.leadTimeDaysVariance;
    const meanDemand = params.dailyDemandMean;
    const meanLeadTime = params.leadTimeDaysMean;

    const totalVariance = meanLeadTime * demandVariance + Math.pow(meanDemand, 2) * leadTimeVariance;
    const combinedStdDev = Math.sqrt(Math.max(0, totalVariance));

    const safetyStockUnits = Math.ceil(zScore * combinedStdDev);
    const reorderPointUnits = Math.ceil(meanDemand * meanLeadTime + safetyStockUnits);

    return {
      safetyStockUnits,
      reorderPointUnits,
      serviceLevelZScore: zScore,
      combinedStandardDeviation: Math.round(combinedStdDev * 100) / 100
    };
  }
}
""")

    print("Production domain matrix generated.")

if __name__ == "__main__":
    generate_prod_domain_matrix()
