import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_core_packages_prod():
    # 1. core-types: Expanded Domain Models & DTOs
    write_file("packages/core-types/src/domain-models.ts", """import { OrderStatus, PaymentStatus, UserRole, FulfillmentStatus, Currency, KycStatus, AccountStatus } from './enums.js';

export interface BaseEntity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date | null;
}

export interface Money {
  amount: number; // in minor currency units (cents, pence)
  currency: Currency;
}

export interface UserEntity extends BaseEntity {
  email: string;
  passwordHash: string;
  role: UserRole;
  status: AccountStatus;
  kycStatus: KycStatus;
  organizationId?: string | null;
  isMfaEnabled: boolean;
  mfaSecret?: string | null;
  failedLoginAttempts: number;
  lockedUntil?: Date | null;
  lastLoginAt?: Date | null;
  passwordChangedAt: Date;
}

export interface UserProfileEntity extends BaseEntity {
  userId: string;
  firstName: string;
  lastName: string;
  phoneNumber?: string | null;
  avatarUrl?: string | null;
  timezone: string;
  locale: string;
  dateOfBirth?: string | null;
  preferences: UserPreferences;
  metadata: Record<string, any>;
}

export interface UserPreferences {
  marketingEmails: boolean;
  orderSmsNotifications: boolean;
  twoFactorRequiredForOrders: boolean;
  preferredCurrency: Currency;
  theme: 'light' | 'dark' | 'system';
}

export interface AddressEntity extends BaseEntity {
  userId: string;
  recipientName: string;
  companyName?: string | null;
  streetLine1: string;
  streetLine2?: string | null;
  city: string;
  stateOrProvince: string;
  postalCode: string;
  countryCode: string;
  isDefaultShipping: boolean;
  isDefaultBilling: boolean;
  phone?: string | null;
  deliveryInstructions?: string | null;
}

export interface OrganizationEntity extends BaseEntity {
  name: string;
  slug: string;
  billingEmail: string;
  tier: 'FREE' | 'STARTER' | 'PRO' | 'ENTERPRISE';
  maxSeats: number;
  isActive: boolean;
  taxIdentifier?: string | null;
  settings: Record<string, any>;
}

export interface OrganizationMemberEntity extends BaseEntity {
  organizationId: string;
  userId: string;
  role: 'OWNER' | 'ADMIN' | 'MEMBER' | 'BILLING_MANAGER' | 'READ_ONLY';
  joinedAt: Date;
}

export interface ProductEntity extends BaseEntity {
  sku: string;
  name: string;
  slug: string;
  description: string;
  categoryId: string;
  basePrice: Money;
  isActive: boolean;
  isFeatured: boolean;
  tags: string[];
  attributes: Record<string, string | number | boolean>;
  images: ProductImageEntity[];
  variants?: ProductVariantEntity[];
}

export interface ProductVariantEntity extends BaseEntity {
  productId: string;
  sku: string;
  name: string;
  priceModifier: Money;
  weightGrams: number;
  dimensionsMm: Dimensions3D;
  options: Record<string, string>;
  isActive: boolean;
}

export interface ProductImageEntity {
  id: string;
  productId?: string;
  url: string;
  altText?: string;
  sortOrder: number;
  isPrimary: boolean;
}

export interface Dimensions3D {
  length: number;
  width: number;
  height: number;
}

export interface CategoryEntity extends BaseEntity {
  name: string;
  slug: string;
  description?: string | null;
  parentId?: string | null;
  displayOrder: number;
  isActive: boolean;
  metaTitle?: string | null;
  metaDescription?: string | null;
}

export interface InventoryStockEntity extends BaseEntity {
  sku: string;
  warehouseId: string;
  onHandQuantity: number;
  reservedQuantity: number;
  allocatedQuantity: number;
  safetyStockThreshold: number;
  reorderQuantity: number;
  binLocation?: string | null;
  version: number;
}

export interface InventoryReservationEntity extends BaseEntity {
  reservationCode: string;
  orderId: string;
  sku: string;
  warehouseId: string;
  quantity: number;
  isCommitted: boolean;
  isReleased: boolean;
  expiresAt: Date;
}

export interface WarehouseEntity extends BaseEntity {
  code: string;
  name: string;
  latitude: number;
  longitude: number;
  address: AddressEntity;
  isActive: boolean;
  capacityScore: number;
}

export interface OrderEntity extends BaseEntity {
  orderNumber: string;
  userId: string;
  status: OrderStatus;
  items: OrderItemEntity[];
  subtotalAmount: Money;
  taxAmount: Money;
  shippingFeeAmount: Money;
  discountAmount: Money;
  totalAmount: Money;
  shippingAddress: AddressEntity;
  billingAddress: AddressEntity;
  couponCode?: string | null;
  paymentId?: string | null;
  shipmentId?: string | null;
  cancellationReason?: string | null;
  notes?: string | null;
  idempotencyKey: string;
}

export interface OrderItemEntity {
  id: string;
  orderId: string;
  sku: string;
  productName: string;
  variantName?: string | null;
  unitPrice: Money;
  quantity: number;
  subtotal: Money;
  taxAmount: Money;
  discountAmount: Money;
  total: Money;
  metadata?: Record<string, any>;
}

export interface PaymentTransactionEntity extends BaseEntity {
  transactionReference: string;
  orderId: string;
  userId: string;
  amount: Money;
  status: PaymentStatus;
  methodType: 'CREDIT_CARD' | 'DEBIT_CARD' | 'BANK_TRANSFER' | 'PAYPAL' | 'APPLE_PAY' | 'GOOGLE_PAY' | 'STORE_CREDIT';
  provider: 'STRIPE' | 'PAYPAL' | 'ADYEN' | 'MOCK' | 'INTERNAL_LEDGER';
  providerTransactionId?: string | null;
  failureReason?: string | null;
  idempotencyKey: string;
  metadata: Record<string, any>;
}

export interface LedgerAccountEntity extends BaseEntity {
  accountNumber: string;
  name: string;
  type: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'EXPENSE';
  currency: Currency;
  balance: number;
}

export interface LedgerJournalEntryEntity extends BaseEntity {
  entryNumber: string;
  description: string;
  transactionId?: string | null;
  referenceType: string;
  referenceId: string;
  lines: LedgerLineEntity[];
  postedAt: Date;
}

export interface LedgerLineEntity {
  id: string;
  journalEntryId: string;
  accountId: string;
  entryType: 'DEBIT' | 'CREDIT';
  amount: number; // in cents
  memo?: string;
}

export interface ShipmentEntity extends BaseEntity {
  shipmentNumber: string;
  orderId: string;
  status: FulfillmentStatus;
  carrier: 'FEDEX' | 'UPS' | 'DHL' | 'USPS' | 'INTERNAL_FLEET' | 'MOCK_CARRIER';
  serviceLevel: string;
  trackingNumber?: string | null;
  trackingUrl?: string | null;
  shippingLabelUrl?: string | null;
  originWarehouseId: string;
  destinationAddress: AddressEntity;
  weightGrams: number;
  dimensionsMm: Dimensions3D;
  dispatchedAt?: Date | null;
  deliveredAt?: Date | null;
}

export interface NotificationLogEntity extends BaseEntity {
  recipient: string;
  channel: 'EMAIL' | 'SMS' | 'PUSH' | 'WEBHOOK';
  templateId: string;
  status: 'PENDING' | 'SENT' | 'DELIVERED' | 'FAILED' | 'BOUNCED';
  payload: Record<string, any>;
  errorDetails?: string | null;
}

export interface AnalyticsEventEntity extends BaseEntity {
  eventName: string;
  userId?: string | null;
  sessionId?: string | null;
  properties: Record<string, any>;
  ipAddress?: string | null;
  userAgent?: string | null;
  timestamp: Date;
}

export interface AuditLogEntity extends BaseEntity {
  serviceName: string;
  action: string;
  actorId: string;
  actorRole: string;
  resourceType: string;
  resourceId: string;
  changes?: Record<string, any> | null;
  timestamp: Date;
}
""")

    print("Generated core-types domain models.")

if __name__ == "__main__":
    generate_core_packages_prod()
