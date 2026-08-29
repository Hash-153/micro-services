import { ProductAttributeSchemaDefinition } from '@novacommerce/core-types';

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
