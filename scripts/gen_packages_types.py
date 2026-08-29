import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_core_types():
    pkg_dir = "packages/core-types"
    
    write_file(f"{pkg_dir}/package.json", """{
  "name": "@novacommerce/core-types",
  "version": "1.0.0",
  "description": "Shared canonical domain types, enums, DTOs, event contracts and errors",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{pkg_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{pkg_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    # Enums
    write_file(f"{pkg_dir}/src/enums/OrderStatus.ts", """export enum OrderStatus {
  DRAFT = 'DRAFT',
  PENDING_PAYMENT = 'PENDING_PAYMENT',
  PAYMENT_AUTHORIZED = 'PAYMENT_AUTHORIZED',
  PAYMENT_FAILED = 'PAYMENT_FAILED',
  PROCESSING = 'PROCESSING',
  INVENTORY_RESERVED = 'INVENTORY_RESERVED',
  INVENTORY_ALLOCATION_FAILED = 'INVENTORY_ALLOCATION_FAILED',
  PACKED = 'PACKED',
  DISPATCHED = 'DISPATCHED',
  IN_TRANSIT = 'IN_TRANSIT',
  OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY',
  DELIVERED = 'DELIVERED',
  CANCELLED = 'CANCELLED',
  REFUND_REQUESTED = 'REFUND_REQUESTED',
  REFUNDED = 'REFUNDED',
  PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED',
  EXPIRED = 'EXPIRED'
}

export enum OrderCancellationReason {
  CUSTOMER_REQUEST = 'CUSTOMER_REQUEST',
  PAYMENT_DECLINED = 'PAYMENT_DECLINED',
  INVENTORY_OUT_OF_STOCK = 'INVENTORY_OUT_OF_STOCK',
  SUSPECTED_FRAUD = 'SUSPECTED_FRAUD',
  CARRIER_RESTRICTION = 'CARRIER_RESTRICTION',
  TIMEOUT_EXPIRED = 'TIMEOUT_EXPIRED',
  SYSTEM_ERROR = 'SYSTEM_ERROR'
}
""")

    write_file(f"{pkg_dir}/src/enums/PaymentStatus.ts", """export enum PaymentStatus {
  PENDING = 'PENDING',
  REQUIRES_ACTION = 'REQUIRES_ACTION',
  PROCESSING = 'PROCESSING',
  AUTHORIZED = 'AUTHORIZED',
  CAPTURED = 'CAPTURED',
  FAILED = 'FAILED',
  CANCELLED = 'CANCELLED',
  REFUNDED = 'REFUNDED',
  PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED',
  DISPUTED = 'DISPUTED',
  CHARGEBACK = 'CHARGEBACK'
}

export enum PaymentMethodType {
  CREDIT_CARD = 'CREDIT_CARD',
  DEBIT_CARD = 'DEBIT_CARD',
  BANK_TRANSFER = 'BANK_TRANSFER',
  PAYPAL = 'PAYPAL',
  APPLE_PAY = 'APPLE_PAY',
  GOOGLE_PAY = 'GOOGLE_PAY',
  CRYPTO = 'CRYPTO',
  STORE_CREDIT = 'STORE_CREDIT',
  GIFT_CARD = 'GIFT_CARD'
}

export enum PaymentGatewayProvider {
  STRIPE = 'STRIPE',
  PAYPAL = 'PAYPAL',
  ADYEN = 'ADYEN',
  MOCK = 'MOCK',
  INTERNAL_LEDGER = 'INTERNAL_LEDGER'
}
""")

    write_file(f"{pkg_dir}/src/enums/UserRole.ts", """export enum UserRole {
  SUPER_ADMIN = 'SUPER_ADMIN',
  ADMIN = 'ADMIN',
  OPERATIONS_MANAGER = 'OPERATIONS_MANAGER',
  INVENTORY_MANAGER = 'INVENTORY_MANAGER',
  FINANCE_ANALYST = 'FINANCE_ANALYST',
  SUPPORT_AGENT = 'SUPPORT_AGENT',
  CUSTOMER = 'CUSTOMER',
  GUEST = 'GUEST',
  SYSTEM_INTERNAL = 'SYSTEM_INTERNAL'
}

export enum AccountStatus {
  ACTIVE = 'ACTIVE',
  PENDING_VERIFICATION = 'PENDING_VERIFICATION',
  SUSPENDED = 'SUSPENDED',
  DEACTIVATED = 'DEACTIVATED',
  LOCKED = 'LOCKED'
}

export enum KycStatus {
  NOT_SUBMITTED = 'NOT_SUBMITTED',
  PENDING_REVIEW = 'PENDING_REVIEW',
  VERIFIED = 'VERIFIED',
  REJECTED = 'REJECTED',
  EXPIRED = 'EXPIRED'
}
""")

    write_file(f"{pkg_dir}/src/enums/FulfillmentStatus.ts", """export enum FulfillmentStatus {
  UNFULFILLED = 'UNFULFILLED',
  ALLOCATING = 'ALLOCATING',
  PICKING = 'PICKING',
  PACKED = 'PACKED',
  LABEL_GENERATED = 'LABEL_GENERATED',
  READY_FOR_PICKUP = 'READY_FOR_PICKUP',
  SHIPPED = 'SHIPPED',
  IN_TRANSIT = 'IN_TRANSIT',
  OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY',
  DELIVERED = 'DELIVERED',
  FAILED_ATTEMPT = 'FAILED_ATTEMPT',
  RETURNED_TO_SENDER = 'RETURNED_TO_SENDER',
  LOST_IN_TRANSIT = 'LOST_IN_TRANSIT'
}

export enum CarrierCode {
  FEDEX = 'FEDEX',
  UPS = 'UPS',
  DHL = 'DHL',
  USPS = 'USPS',
  INTERNAL_FLEET = 'INTERNAL_FLEET',
  MOCK_CARRIER = 'MOCK_CARRIER'
}
""")

    write_file(f"{pkg_dir}/src/enums/Currency.ts", """export enum Currency {
  USD = 'USD',
  EUR = 'EUR',
  GBP = 'GBP',
  CAD = 'CAD',
  AUD = 'AUD',
  JPY = 'JPY',
  CHF = 'CHF',
  SGD = 'SGD',
  INR = 'INR'
}

export interface Money {
  amount: number; // Stored in minor currency units (cents, pence, etc.)
  currency: Currency;
}
""")

    write_file(f"{pkg_dir}/src/enums/EventType.ts", """export enum EventType {
  // Auth Events
  AUTH_USER_REGISTERED = 'auth.user.registered',
  AUTH_USER_LOGGED_IN = 'auth.user.logged_in',
  AUTH_PASSWORD_RESET_REQUESTED = 'auth.password.reset_requested',
  AUTH_PASSWORD_RESET_COMPLETED = 'auth.password.reset_completed',
  AUTH_MFA_ENABLED = 'auth.mfa.enabled',
  AUTH_MFA_DISABLED = 'auth.mfa.disabled',
  AUTH_TOKEN_REVOKED = 'auth.token.revoked',

  // User Profile Events
  USER_PROFILE_UPDATED = 'user.profile.updated',
  USER_ADDRESS_ADDED = 'user.address.added',
  USER_ADDRESS_REMOVED = 'user.address.removed',
  USER_KYC_VERIFIED = 'user.kyc.verified',
  USER_ORGANIZATION_JOINED = 'user.org.joined',

  // Catalog Events
  CATALOG_PRODUCT_CREATED = 'catalog.product.created',
  CATALOG_PRODUCT_UPDATED = 'catalog.product.updated',
  CATALOG_PRODUCT_DELETED = 'catalog.product.deleted',
  CATALOG_PRICE_CHANGED = 'catalog.price.changed',
  CATALOG_CATEGORY_CREATED = 'catalog.category.created',

  // Inventory Events
  INVENTORY_STOCK_UPDATED = 'inventory.stock.updated',
  INVENTORY_RESERVATION_CREATED = 'inventory.reservation.created',
  INVENTORY_RESERVATION_RELEASED = 'inventory.reservation.released',
  INVENTORY_RESERVATION_COMMITTED = 'inventory.reservation.committed',
  INVENTORY_LOW_STOCK_ALERT = 'inventory.stock.low_alert',
  INVENTORY_REORDER_TRIGGERED = 'inventory.reorder.triggered',

  // Order & Saga Events
  ORDER_CREATED = 'order.created',
  ORDER_UPDATED = 'order.updated',
  ORDER_SUBMITTED = 'order.submitted',
  ORDER_PAYMENT_PENDING = 'order.payment_pending',
  ORDER_PAID = 'order.paid',
  ORDER_FULFILLED = 'order.fulfilled',
  ORDER_COMPLETED = 'order.completed',
  ORDER_CANCELLED = 'order.cancelled',
  ORDER_REFUND_INITIATED = 'order.refund.initiated',
  ORDER_SAGA_STARTED = 'order.saga.started',
  ORDER_SAGA_COMPLETED = 'order.saga.completed',
  ORDER_SAGA_COMPENSATING = 'order.saga.compensating',
  ORDER_SAGA_FAILED = 'order.saga.failed',

  // Payment Events
  PAYMENT_INTENT_CREATED = 'payment.intent.created',
  PAYMENT_AUTHORIZED = 'payment.authorized',
  PAYMENT_CAPTURED = 'payment.captured',
  PAYMENT_FAILED = 'payment.failed',
  PAYMENT_REFUNDED = 'payment.refunded',
  PAYMENT_DISPUTED = 'payment.disputed',
  LEDGER_ENTRY_RECORDED = 'payment.ledger.recorded',

  // Fulfillment Events
  FULFILLMENT_CREATED = 'fulfillment.created',
  FULFILLMENT_LABEL_GENERATED = 'fulfillment.label_generated',
  FULFILLMENT_DISPATCHED = 'fulfillment.dispatched',
  FULFILLMENT_IN_TRANSIT = 'fulfillment.in_transit',
  FULFILLMENT_DELIVERED = 'fulfillment.delivered',
  FULFILLMENT_FAILED = 'fulfillment.failed',

  // Notification Events
  NOTIFICATION_REQUESTED = 'notification.requested',
  NOTIFICATION_SENT = 'notification.sent',
  NOTIFICATION_FAILED = 'notification.failed',
  NOTIFICATION_BOUNCED = 'notification.bounced',

  // Analytics & Audit Events
  ANALYTICS_EVENT_INGESTED = 'analytics.event.ingested',
  AUDIT_LOG_RECORDED = 'analytics.audit.recorded'
}
""")

    write_file(f"{pkg_dir}/src/enums/ErrorCode.ts", """export enum ErrorCode {
  // Generic
  INTERNAL_SERVER_ERROR = 'ERR_INTERNAL_SERVER_ERROR',
  VALIDATION_ERROR = 'ERR_VALIDATION_ERROR',
  BAD_REQUEST = 'ERR_BAD_REQUEST',
  UNAUTHORIZED = 'ERR_UNAUTHORIZED',
  FORBIDDEN = 'ERR_FORBIDDEN',
  NOT_FOUND = 'ERR_NOT_FOUND',
  CONFLICT = 'ERR_CONFLICT',
  RATE_LIMIT_EXCEEDED = 'ERR_RATE_LIMIT_EXCEEDED',
  SERVICE_UNAVAILABLE = 'ERR_SERVICE_UNAVAILABLE',
  GATEWAY_TIMEOUT = 'ERR_GATEWAY_TIMEOUT',

  // Auth
  INVALID_CREDENTIALS = 'ERR_AUTH_INVALID_CREDENTIALS',
  TOKEN_EXPIRED = 'ERR_AUTH_TOKEN_EXPIRED',
  TOKEN_INVALID = 'ERR_AUTH_TOKEN_INVALID',
  ACCOUNT_LOCKED = 'ERR_AUTH_ACCOUNT_LOCKED',
  ACCOUNT_DISABLED = 'ERR_AUTH_ACCOUNT_DISABLED',
  MFA_REQUIRED = 'ERR_AUTH_MFA_REQUIRED',
  MFA_INVALID_CODE = 'ERR_AUTH_MFA_INVALID_CODE',
  PASSWORD_TOO_WEAK = 'ERR_AUTH_PASSWORD_TOO_WEAK',

  // Inventory
  INSUFFICIENT_STOCK = 'ERR_INVENTORY_INSUFFICIENT_STOCK',
  RESERVATION_EXPIRED = 'ERR_INVENTORY_RESERVATION_EXPIRED',
  WAREHOUSE_UNAVAILABLE = 'ERR_INVENTORY_WAREHOUSE_UNAVAILABLE',

  // Order & Saga
  ORDER_INVALID_STATE_TRANSITION = 'ERR_ORDER_INVALID_STATE_TRANSITION',
  ORDER_ALREADY_PAID = 'ERR_ORDER_ALREADY_PAID',
  ORDER_ALREADY_CANCELLED = 'ERR_ORDER_ALREADY_CANCELLED',
  SAGA_EXECUTION_FAILED = 'ERR_SAGA_EXECUTION_FAILED',
  SAGA_COMPENSATION_FAILED = 'ERR_SAGA_COMPENSATION_FAILED',

  // Payment
  PAYMENT_DECLINED = 'ERR_PAYMENT_DECLINED',
  PAYMENT_METHOD_INVALID = 'ERR_PAYMENT_METHOD_INVALID',
  GATEWAY_COMMUNICATION_ERROR = 'ERR_PAYMENT_GATEWAY_ERROR',
  LEDGER_UNBALANCED_ENTRY = 'ERR_PAYMENT_LEDGER_UNBALANCED',
  REFUND_EXCEEDS_ORIGINAL = 'ERR_PAYMENT_REFUND_EXCEEDS_ORIGINAL',

  // Fulfillment
  CARRIER_RATE_UNAVAILABLE = 'ERR_FULFILLMENT_CARRIER_RATE_UNAVAILABLE',
  ADDRESS_UNVERIFIED = 'ERR_FULFILLMENT_ADDRESS_UNVERIFIED',
  PACKAGE_OVERSIZED = 'ERR_FULFILLMENT_PACKAGE_OVERSIZED'
}
""")

    # Models & Entities
    write_file(f"{pkg_dir}/src/models/User.ts", """import { UserRole, AccountStatus, KycStatus } from '../enums/UserRole.js';

export interface UserEntity {
  id: string;
  email: string;
  passwordHash: string;
  role: UserRole;
  status: AccountStatus;
  kycStatus: KycStatus;
  organizationId?: string;
  isMfaEnabled: boolean;
  mfaSecret?: string;
  failedLoginAttempts: number;
  lockedUntil?: Date;
  lastLoginAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date;
}

export interface UserProfileEntity {
  id: string;
  userId: string;
  firstName: string;
  lastName: string;
  phoneNumber?: string;
  avatarUrl?: string;
  timeZone: string;
  locale: string;
  metadata: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

export interface AddressEntity {
  id: string;
  userId: string;
  recipientName: string;
  streetLine1: string;
  streetLine2?: string;
  city: string;
  stateOrProvince: string;
  postalCode: string;
  countryCode: string; // ISO 3166-1 alpha-2 (e.g. US, DE, GB)
  isDefaultShipping: boolean;
  isDefaultBilling: boolean;
  phone?: string;
  createdAt: Date;
  updatedAt: Date;
}
""")

    write_file(f"{pkg_dir}/src/models/Product.ts", """import { Money } from '../enums/Currency.js';

export interface ProductEntity {
  id: string;
  sku: string;
  name: string;
  slug: string;
  description: string;
  categoryId: string;
  basePrice: Money;
  isActive: boolean;
  tags: string[];
  attributes: Record<string, string | number | boolean>;
  images: ProductImage[];
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date;
}

export interface ProductImage {
  id: string;
  url: string;
  altText?: string;
  sortOrder: number;
  isPrimary: boolean;
}

export interface ProductVariantEntity {
  id: string;
  productId: string;
  sku: string;
  name: string;
  priceModifier: number; // in cents
  weightGrams: number;
  dimensionsMm: {
    length: number;
    width: number;
    height: number;
  };
  options: Record<string, string>; // e.g. { "size": "XL", "color": "Navy" }
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface CategoryEntity {
  id: string;
  name: string;
  slug: string;
  description?: string;
  parentId?: string;
  displayOrder: number;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}
""")

    write_file(f"{pkg_dir}/src/models/Inventory.ts", """export interface InventoryStockEntity {
  id: string;
  sku: string;
  warehouseId: string;
  onHandQuantity: number;
  reservedQuantity: number;
  allocatedQuantity: number;
  safetyStockThreshold: number;
  reorderQuantity: number;
  binLocation?: string;
  version: number; // Optimistic locking
  updatedAt: Date;
}

export interface InventoryReservationEntity {
  id: string;
  reservationCode: string;
  orderId: string;
  sku: string;
  warehouseId: string;
  quantity: number;
  isCommitted: boolean;
  isReleased: boolean;
  expiresAt: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface WarehouseEntity {
  id: string;
  code: string;
  name: string;
  addressId: string;
  isActive: boolean;
  capacityScore: number;
  createdAt: Date;
  updatedAt: Date;
}
""")

    write_file(f"{pkg_dir}/src/models/Order.ts", """import { OrderStatus, OrderCancellationReason } from '../enums/OrderStatus.js';
import { Money } from '../enums/Currency.js';
import { AddressEntity } from './User.js';

export interface OrderItemEntity {
  id: string;
  orderId: string;
  sku: string;
  productName: string;
  variantName?: string;
  unitPrice: Money;
  quantity: number;
  subtotal: Money;
  taxAmount: Money;
  discountAmount: Money;
  total: Money;
  metadata?: Record<string, unknown>;
}

export interface OrderEntity {
  id: string;
  orderNumber: string;
  userId: string;
  status: OrderStatus;
  shippingAddress: AddressEntity;
  billingAddress: AddressEntity;
  items: OrderItemEntity[];
  subtotalAmount: Money;
  taxAmount: Money;
  shippingFeeAmount: Money;
  discountAmount: Money;
  totalAmount: Money;
  couponCode?: string;
  paymentId?: string;
  shipmentId?: string;
  cancellationReason?: OrderCancellationReason;
  notes?: string;
  idempotencyKey?: string;
  createdAt: Date;
  updatedAt: Date;
}
""")

    write_file(f"{pkg_dir}/src/models/Payment.ts", """import { PaymentStatus, PaymentMethodType, PaymentGatewayProvider } from '../enums/PaymentStatus.js';
import { Money } from '../enums/Currency.js';

export interface PaymentTransactionEntity {
  id: string;
  transactionReference: string;
  orderId: string;
  userId: string;
  amount: Money;
  status: PaymentStatus;
  methodType: PaymentMethodType;
  provider: PaymentGatewayProvider;
  providerTransactionId?: string;
  failureReason?: string;
  idempotencyKey: string;
  metadata: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

export interface LedgerAccountEntity {
  id: string;
  accountNumber: string;
  name: string;
  type: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'EXPENSE';
  currency: string;
  balance: number; // in cents
  createdAt: Date;
  updatedAt: Date;
}

export interface LedgerJournalEntryEntity {
  id: string;
  entryNumber: string;
  description: string;
  transactionId?: string;
  referenceType: string;
  referenceId: string;
  postedAt: Date;
  lines: LedgerLineEntity[];
}

export interface LedgerLineEntity {
  id: string;
  journalEntryId: string;
  accountId: string;
  entryType: 'DEBIT' | 'CREDIT';
  amount: number; // in cents
  memo?: string;
}
""")

    write_file(f"{pkg_dir}/src/models/Shipment.ts", """import { FulfillmentStatus, CarrierCode } from '../enums/FulfillmentStatus.js';
import { AddressEntity } from './User.js';

export interface ShipmentEntity {
  id: string;
  shipmentNumber: string;
  orderId: string;
  status: FulfillmentStatus;
  carrier: CarrierCode;
  serviceLevel: string; // e.g. 'STANDARD_GROUND', 'EXPRESS_2_DAY', 'OVERNIGHT'
  trackingNumber?: string;
  trackingUrl?: string;
  shippingLabelUrl?: string;
  originWarehouseId: string;
  destinationAddress: AddressEntity;
  weightGrams: number;
  dimensionsMm: {
    length: number;
    width: number;
    height: number;
  };
  dispatchedAt?: Date;
  deliveredAt?: Date;
  createdAt: Date;
  updatedAt: Date;
}
""")

    # DTOs
    write_file(f"{pkg_dir}/src/dto/AuthDTO.ts", """import { z } from 'zod';
import { UserRole } from '../enums/UserRole.js';

export const RegisterUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]/, {
    message: 'Password must contain uppercase, lowercase, number and special symbol.'
  }),
  firstName: z.string().min(1).max(50),
  lastName: z.string().min(1).max(50),
  role: z.nativeEnum(UserRole).optional().default(UserRole.CUSTOMER),
  phoneNumber: z.string().optional()
});

export type RegisterUserDTO = z.infer<typeof RegisterUserSchema>;

export const LoginUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
  mfaCode: z.string().length(6).optional()
});

export type LoginUserDTO = z.infer<typeof LoginUserSchema>;

export const RefreshTokenSchema = z.object({
  refreshToken: z.string().min(1)
});

export type RefreshTokenDTO = z.infer<typeof RefreshTokenSchema>;

export interface AuthTokensResponseDTO {
  accessToken: string;
  refreshToken: string;
  expiresInSeconds: number;
  tokenType: 'Bearer';
  user: {
    id: string;
    email: string;
    role: UserRole;
    firstName: string;
    lastName: string;
  };
}
""")

    write_file(f"{pkg_dir}/src/dto/OrderDTO.ts", """import { z } from 'zod';
import { Currency } from '../enums/Currency.js';

export const OrderItemInputSchema = z.object({
  sku: z.string().min(1),
  quantity: z.number().int().positive()
});

export const CreateOrderSchema = z.object({
  userId: z.string().uuid().optional(),
  shippingAddressId: z.string().uuid(),
  billingAddressId: z.string().uuid(),
  items: z.array(OrderItemInputSchema).min(1),
  currency: z.nativeEnum(Currency).default(Currency.USD),
  couponCode: z.string().optional(),
  notes: z.string().max(500).optional(),
  idempotencyKey: z.string().uuid()
});

export type CreateOrderDTO = z.infer<typeof CreateOrderSchema>;

export const CheckoutSagaRequestSchema = z.object({
  orderId: z.string().uuid(),
  paymentMethod: z.object({
    type: z.string(),
    token: z.string(),
    provider: z.string()
  }),
  carrierCode: z.string().default('MOCK_CARRIER'),
  idempotencyKey: z.string().uuid()
});

export type CheckoutSagaRequestDTO = z.infer<typeof CheckoutSagaRequestSchema>;
""")

    write_file(f"{pkg_dir}/src/dto/ProductDTO.ts", """import { z } from 'zod';
import { Currency } from '../enums/Currency.js';

export const CreateProductSchema = z.object({
  sku: z.string().min(3).max(64),
  name: z.string().min(1).max(255),
  slug: z.string().min(1).max(255),
  description: z.string().max(4000),
  categoryId: z.string().uuid(),
  basePrice: z.object({
    amount: z.number().int().nonnegative(),
    currency: z.nativeEnum(Currency)
  }),
  tags: z.array(z.string()).default([]),
  attributes: z.record(z.union([z.string(), z.number(), z.boolean()])).default({}),
  isActive: z.boolean().default(true)
});

export type CreateProductDTO = z.infer<typeof CreateProductSchema>;

export const ProductFilterQuerySchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(20),
  categoryId: z.string().uuid().optional(),
  search: z.string().optional(),
  minPrice: z.coerce.number().int().optional(),
  maxPrice: z.coerce.number().int().optional(),
  tags: z.string().optional(), // comma-separated
  sortBy: z.enum(['price_asc', 'price_desc', 'created_desc', 'name_asc']).default('created_desc')
});

export type ProductFilterQueryDTO = z.infer<typeof ProductFilterQuerySchema>;
""")

    # Errors
    write_file(f"{pkg_dir}/src/errors/AppError.ts", """import { ErrorCode } from '../enums/ErrorCode.js';

export class AppError extends Error {
  public readonly statusCode: number;
  public readonly code: ErrorCode;
  public readonly isOperational: boolean;
  public readonly details?: Record<string, unknown> | unknown[];

  constructor(
    message: string,
    statusCode: number = 500,
    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR,
    details?: Record<string, unknown> | unknown[],
    isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: Record<string, unknown> | unknown[]) {
    super(message, 400, ErrorCode.VALIDATION_ERROR, details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, identifier?: string) {
    const message = identifier ? `${resource} with id '${identifier}' was not found.` : `${resource} was not found.`;
    super(message, 404, ErrorCode.NOT_FOUND, { resource, identifier });
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Authentication credentials are invalid or missing.') {
    super(message, 401, ErrorCode.UNAUTHORIZED);
  }
}

export class ForbiddenError extends AppError {
  constructor(message: string = 'You do not possess sufficient permissions to perform this operation.') {
    super(message, 403, ErrorCode.FORBIDDEN);
  }
}

export class ConflictError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 409, ErrorCode.CONFLICT, details);
  }
}

export class InsufficientStockError extends AppError {
  constructor(sku: string, requested: number, available: number) {
    super(`Insufficient stock for SKU '${sku}'. Requested: ${requested}, Available: ${available}`, 400, ErrorCode.INSUFFICIENT_STOCK, {
      sku,
      requested,
      available
    });
  }
}

export class SagaExecutionError extends AppError {
  constructor(sagaName: string, stepFailed: string, originalError: Error) {
    super(`Saga '${sagaName}' failed at step '${stepFailed}': ${originalError.message}`, 500, ErrorCode.SAGA_EXECUTION_FAILED, {
      sagaName,
      stepFailed,
      originalMessage: originalError.message
    });
  }
}
""")

    # HTTP Response Contracts
    write_file(f"{pkg_dir}/src/http/ApiResponse.ts", """export interface ApiResponse<T = unknown> {
  success: boolean;
  statusCode: number;
  data: T;
  meta?: ResponseMetadata;
}

export interface ApiErrorResponse {
  success: false;
  statusCode: number;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown> | unknown[];
    correlationId?: string;
    timestamp: string;
  };
}

export interface ResponseMetadata {
  page?: number;
  limit?: number;
  totalItems?: number;
  totalPages?: number;
  hasNextPage?: boolean;
  hasPrevPage?: boolean;
  correlationId?: string;
  executionTimeMs?: number;
}
""")

    # Events Interface
    write_file(f"{pkg_dir}/src/events/DomainEvent.ts", """import { EventType } from '../enums/EventType.js';

export interface DomainEvent<T = unknown> {
  id: string;
  eventType: EventType;
  aggregateId: string;
  aggregateType: string;
  version: number;
  timestamp: string;
  correlationId: string;
  causationId?: string;
  producer: string;
  payload: T;
}

export interface OutboxEventRecord {
  id: string;
  aggregateType: string;
  aggregateId: string;
  eventType: string;
  payload: string; // JSON stringified
  correlationId: string;
  status: 'PENDING' | 'PUBLISHED' | 'FAILED';
  retryCount: number;
  lastError?: string;
  createdAt: Date;
  processedAt?: Date;
}
""")

    # Index
    write_file(f"{pkg_dir}/src/index.ts", """// Enums
export * from './enums/OrderStatus.js';
export * from './enums/PaymentStatus.js';
export * from './enums/UserRole.js';
export * from './enums/FulfillmentStatus.js';
export * from './enums/Currency.js';
export * from './enums/EventType.js';
export * from './enums/ErrorCode.js';

// Models
export * from './models/User.js';
export * from './models/Product.js';
export * from './models/Inventory.js';
export * from './models/Order.js';
export * from './models/Payment.js';
export * from './models/Shipment.js';

// DTOs
export * from './dto/AuthDTO.js';
export * from './dto/OrderDTO.js';
export * from './dto/ProductDTO.js';

// Errors
export * from './errors/AppError.js';

// HTTP
export * from './http/ApiResponse.js';

// Events
export * from './events/DomainEvent.js';
""")

    # Tests
    write_file(f"{pkg_dir}/tests/types.test.ts", """import { OrderStatus, PaymentStatus, UserRole, ErrorCode } from '../src/index.js';
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
""")

    print(f"Generated {pkg_dir}")

if __name__ == "__main__":
    generate_core_types()
