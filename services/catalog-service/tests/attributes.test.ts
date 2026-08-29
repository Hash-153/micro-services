import { ProductAttributeValidator, AttributeSchemaField } from '../src/domain/attribute-validator.js';

describe('Product Dynamic Attribute Validation Suite', () => {
  const schema: AttributeSchemaField[] = [
    { name: 'screenSizeInches', label: 'Screen Size', type: 'NUMBER', required: true, minValue: 5, maxValue: 100 },
    { name: 'color', label: 'Color', type: 'ENUM', required: true, allowedValues: ['Black', 'Silver', 'Space Gray'] },
    { name: 'hasTouchScreen', label: 'Touch Screen', type: 'BOOLEAN', required: false }
  ];

  it('should validate valid attributes', () => {
    const res = ProductAttributeValidator.validate(schema, {
      screenSizeInches: 15.6,
      color: 'Space Gray',
      hasTouchScreen: true
    });
    expect(res.isValid).toBe(true);
    expect(res.errors.length).toBe(0);
  });

  it('should report errors on missing required attribute or illegal enum value', () => {
    const res = ProductAttributeValidator.validate(schema, {
      screenSizeInches: 15.6,
      color: 'Hot Pink' // not in enum
    });
    expect(res.isValid).toBe(false);
    expect(res.errors.some(e => e.includes('Hot Pink'))).toBe(true);
  });
});
