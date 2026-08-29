import { OrderStatus, PaymentStatus, UserRole, ErrorCode } from '../src/index.js';
import { RegisterUserSchema, CreateOrderSchema } from '../src/index.js';
import { AppError, ValidationError } from '../src/index.js';

describe('Core Types & Schemas', () => {
  it('should validate complete enum mappings', () => {
    expect(OrderStatus.PENDING_PAYMENT).toBe('PENDING_PAYMENT');
    expect(PaymentStatus.AUTHORIZED).toBe('AUTHORIZED');
    expect(UserRole.SUPER_ADMIN).toBe('SUPER_ADMIN');
    expect(ErrorCode.INSUFFICIENT_STOCK).toBe('ERR_INVENTORY_INSUFFICIENT_STOCK');
  });

  it('should validate valid user registration payload', () => {
    const validPayload = {
      email: 'john.doe@example.com',
      password: 'SecurePassword123!',
      firstName: 'John',
      lastName: 'Doe',
      role: UserRole.CUSTOMER
    };
    const result = RegisterUserSchema.safeParse(validPayload);
    expect(result.success).toBe(true);
  });

  it('should reject invalid password in user registration', () => {
    const invalidPayload = {
      email: 'john.doe@example.com',
      password: 'weak',
      firstName: 'John',
      lastName: 'Doe'
    };
    const result = RegisterUserSchema.safeParse(invalidPayload);
    expect(result.success).toBe(false);
  });

  it('should instantiate and format domain errors correctly', () => {
    const err = new ValidationError('Field is invalid', { field: 'email' });
    expect(err.statusCode).toBe(400);
    expect(err.code).toBe(ErrorCode.VALIDATION_ERROR);
    expect(err.details).toEqual({ field: 'email' });
  });
});
