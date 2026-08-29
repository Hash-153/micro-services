import { UserRole, OrderStatus, PaymentStatus, FulfillmentStatus, Currency, KycStatus, AccountStatus } from './enums.js';
import { Money, AddressEntity, Dimensions3D } from './domain-models.js';

export interface RegisterUserDTO {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role?: UserRole;
  organizationName?: string;
  phoneNumber?: string;
}

export interface LoginUserDTO {
  email: string;
  password: string;
  mfaCode?: string;
  deviceFingerprint?: string;
}

export interface AuthTokensResponseDTO {
  accessToken: string;
  refreshToken: string;
  tokenType: 'Bearer';
  expiresIn: number;
  user: {
    id: string;
    email: string;
    role: UserRole;
    status: AccountStatus;
    organizationId?: string | null;
  };
}

export interface RefreshTokenDTO {
  refreshToken: string;
}

export interface CreateProductDTO {
  sku: string;
  name: string;
  description: string;
  categoryId: string;
  basePrice: Money;
  tags?: string[];
  attributes?: Record<string, any>;
  images?: { url: string; altText?: string; isPrimary: boolean; sortOrder: number }[];
}

export interface UpdateProductDTO {
  name?: string;
  description?: string;
  categoryId?: string;
  basePrice?: Money;
  isActive?: boolean;
  isFeatured?: boolean;
  tags?: string[];
  attributes?: Record<string, any>;
}

export interface CreateOrderDTO {
  userId: string;
  items: {
    sku: string;
    productName: string;
    variantName?: string;
    quantity: number;
    unitPrice: Money;
  }[];
  shippingAddress: AddressEntity;
  billingAddress: AddressEntity;
  couponCode?: string;
  idempotencyKey: string;
}

export interface AuthorizePaymentDTO {
  orderId: string;
  userId: string;
  amount: Money;
  methodType: 'CREDIT_CARD' | 'DEBIT_CARD' | 'BANK_TRANSFER' | 'PAYPAL' | 'APPLE_PAY';
  paymentMethodToken: string;
  idempotencyKey: string;
}

export interface CreateShipmentDTO {
  orderId: string;
  destinationAddress: AddressEntity;
  carrier: 'FEDEX' | 'UPS' | 'DHL' | 'USPS';
  serviceLevel: string;
  weightGrams: number;
  dimensionsMm: Dimensions3D;
}
