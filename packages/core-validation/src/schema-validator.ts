export interface ValidationSchema {
  type: 'object' | 'array' | 'string' | 'number' | 'boolean' | 'null';
  properties?: Record<string, ValidationSchema>;
  items?: ValidationSchema;
  required?: string[];
  minLength?: number;
  maxLength?: number;
  minimum?: number;
  maximum?: number;
  pattern?: string;
  enum?: any[];
  format?: 'email' | 'uri' | 'uuid' | 'date-time' | 'date';
  additionalProperties?: boolean | ValidationSchema;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
}

export interface ValidationError {
  path: string;
  message: string;
  value: any;
}

export class SchemaValidator {
  public validate(data: any, schema: ValidationSchema): ValidationResult {
    const errors: ValidationError[] = [];
    this.validateValue(data, schema, '', errors);
    
    return {
      valid: errors.length === 0,
      errors
    };
  }

  private validateValue(value: any, schema: ValidationSchema, path: string, errors: ValidationError[]): void {
    // Type validation
    if (!this.validateType(value, schema.type)) {
      errors.push({
        path,
        message: `Expected type ${schema.type}, got ${typeof value}`,
        value
      });
      return;
    }

    // String validation
    if (schema.type === 'string' && typeof value === 'string') {
      if (schema.minLength !== undefined && value.length < schema.minLength) {
        errors.push({
          path,
          message: `String must be at least ${schema.minLength} characters`,
          value
        });
      }
      if (schema.maxLength !== undefined && value.length > schema.maxLength) {
        errors.push({
          path,
          message: `String must be at most ${schema.maxLength} characters`,
          value
        });
      }
      if (schema.pattern && !new RegExp(schema.pattern).test(value)) {
        errors.push({
          path,
          message: `String does not match pattern ${schema.pattern}`,
          value
        });
      }
      if (schema.format && !this.validateFormat(value, schema.format)) {
        errors.push({
          path,
          message: `String does not match format ${schema.format}`,
          value
        });
      }
    }

    // Number validation
    if (schema.type === 'number' && typeof value === 'number') {
      if (schema.minimum !== undefined && value < schema.minimum) {
        errors.push({
          path,
          message: `Number must be at least ${schema.minimum}`,
          value
        });
      }
      if (schema.maximum !== undefined && value > schema.maximum) {
        errors.push({
          path,
          message: `Number must be at most ${schema.maximum}`,
          value
        });
      }
    }

    // Enum validation
    if (schema.enum && !schema.enum.includes(value)) {
      errors.push({
        path,
        message: `Value must be one of: ${schema.enum.join(', ')}`,
        value
      });
    }

    // Object validation
    if (schema.type === 'object' && typeof value === 'object' && value !== null && !Array.isArray(value)) {
      // Required properties
      if (schema.required) {
        for (const prop of schema.required) {
          if (!(prop in value)) {
            errors.push({
              path: `${path}.${prop}`,
              message: `Required property missing`,
              value: undefined
            });
          }
        }
      }

      // Property validation
      if (schema.properties) {
        for (const [prop, propSchema] of Object.entries(schema.properties)) {
          if (prop in value) {
            this.validateValue(value[prop], propSchema, `${path}.${prop}`, errors);
          }
        }
      }

      // Additional properties
      if (schema.additionalProperties === false) {
        for (const prop of Object.keys(value)) {
          if (!schema.properties || !(prop in schema.properties)) {
            errors.push({
              path: `${path}.${prop}`,
              message: `Additional property not allowed`,
              value: value[prop]
            });
          }
        }
      } else if (typeof schema.additionalProperties === 'object') {
        for (const prop of Object.keys(value)) {
          if (!schema.properties || !(prop in schema.properties)) {
            this.validateValue(value[prop], schema.additionalProperties, `${path}.${prop}`, errors);
          }
        }
      }
    }

    // Array validation
    if (schema.type === 'array' && Array.isArray(value)) {
      if (schema.minLength !== undefined && value.length < schema.minLength) {
        errors.push({
          path,
          message: `Array must have at least ${schema.minLength} items`,
          value
        });
      }
      if (schema.maxLength !== undefined && value.length > schema.maxLength) {
        errors.push({
          path,
          message: `Array must have at most ${schema.maxLength} items`,
          value
        });
      }
      if (schema.items) {
        value.forEach((item, index) => {
          this.validateValue(item, schema.items!, `${path}[${index}]`, errors);
        });
      }
    }
  }

  private validateType(value: any, type: string): boolean {
    switch (type) {
      case 'string':
        return typeof value === 'string';
      case 'number':
        return typeof value === 'number';
      case 'boolean':
        return typeof value === 'boolean';
      case 'null':
        return value === null;
      case 'object':
        return typeof value === 'object' && value !== null && !Array.isArray(value);
      case 'array':
        return Array.isArray(value);
      default:
        return true;
    }
  }

  private validateFormat(value: string, format: string): boolean {
    switch (format) {
      case 'email':
        return value.includes('@') && value.includes('.');
      case 'uri':
        try {
          new URL(value);
          return true;
        } catch {
          return false;
        }
      case 'uuid':
        return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
      case 'date-time':
        return !isNaN(Date.parse(value));
      case 'date':
        return value.length === 10 && value[4] === '-' && value[7] === '-';
      default:
        return true;
    }
  }
}
