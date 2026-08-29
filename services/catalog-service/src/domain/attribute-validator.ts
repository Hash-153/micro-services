export type AttributeDataType = 'STRING' | 'NUMBER' | 'BOOLEAN' | 'ENUM' | 'DIMENSIONS';

export interface AttributeSchemaField {
  name: string;
  label: string;
  type: AttributeDataType;
  required: boolean;
  allowedValues?: string[];
  minValue?: number;
  maxValue?: number;
  regexPattern?: string;
}

export class ProductAttributeValidator {
  public static validate(schema: AttributeSchemaField[], attributes: Record<string, unknown>): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    for (const field of schema) {
      const val = attributes[field.name];

      if (field.required && (val === undefined || val === null || val === '')) {
        errors.push(`Attribute '${field.name}' (${field.label}) is required.`);
        continue;
      }

      if (val === undefined || val === null) continue;

      if (field.type === 'NUMBER' && typeof val !== 'number') {
        errors.push(`Attribute '${field.name}' must be a numeric value.`);
      }

      if (field.type === 'BOOLEAN' && typeof val !== 'boolean') {
        errors.push(`Attribute '${field.name}' must be boolean true/false.`);
      }

      if (field.type === 'ENUM' && field.allowedValues && !field.allowedValues.includes(String(val))) {
        errors.push(`Attribute '${field.name}' value '${val}' is not in allowed list [${field.allowedValues.join(', ')}].`);
      }

      if (field.type === 'NUMBER' && typeof val === 'number') {
        if (field.minValue !== undefined && val < field.minValue) {
          errors.push(`Attribute '${field.name}' is below minimum allowed value ${field.minValue}.`);
        }
        if (field.maxValue !== undefined && val > field.maxValue) {
          errors.push(`Attribute '${field.name}' exceeds maximum allowed value ${field.maxValue}.`);
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}
