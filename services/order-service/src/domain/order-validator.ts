import { OrderEntity, OrderItemEntity, AddressEntity } from '@novacommerce/core-types';

export interface ValidationIssue {
  field: string;
  code: string;
  message: string;
}

export class OrderValidator {
  public static validate(order: Partial<OrderEntity>): { isValid: boolean; issues: ValidationIssue[] } {
    const issues: ValidationIssue[] = [];

    if (!order.userId || order.userId.trim().length === 0) {
      issues.push({ field: 'userId', code: 'REQUIRED', message: 'User ID is mandatory for order placement.' });
    }

    if (!order.items || order.items.length === 0) {
      issues.push({ field: 'items', code: 'EMPTY_CART', message: 'Order must contain at least one line item.' });
    } else {
      order.items.forEach((item, idx) => {
        if (!item.sku || item.sku.trim().length === 0) {
          issues.push({ field: `items[${idx}].sku`, code: 'INVALID_SKU', message: 'Item SKU cannot be empty.' });
        }
        if (item.quantity <= 0) {
          issues.push({ field: `items[${idx}].quantity`, code: 'INVALID_QTY', message: 'Quantity must be at least 1 unit.' });
        }
        if (item.unitPrice.amount < 0) {
          issues.push({ field: `items[${idx}].unitPrice`, code: 'INVALID_PRICE', message: 'Unit price cannot be negative.' });
        }
      });
    }

    if (!order.shippingAddress) {
      issues.push({ field: 'shippingAddress', code: 'REQUIRED', message: 'Shipping address is required.' });
    } else {
      this.validateAddress(order.shippingAddress, 'shippingAddress', issues);
    }

    if (!order.billingAddress) {
      issues.push({ field: 'billingAddress', code: 'REQUIRED', message: 'Billing address is required.' });
    } else {
      this.validateAddress(order.billingAddress, 'billingAddress', issues);
    }

    if (order.totalAmount && order.totalAmount.amount < 0) {
      issues.push({ field: 'totalAmount', code: 'INVALID_TOTAL', message: 'Total order amount cannot be negative.' });
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  }

  private static validateAddress(address: AddressEntity, prefix: string, issues: ValidationIssue[]): void {
    if (!address.recipientName || address.recipientName.trim().length === 0) {
      issues.push({ field: `${prefix}.recipientName`, code: 'REQUIRED', message: 'Recipient name is required.' });
    }
    if (!address.streetLine1 || address.streetLine1.trim().length === 0) {
      issues.push({ field: `${prefix}.streetLine1`, code: 'REQUIRED', message: 'Street address line 1 is required.' });
    }
    if (!address.city || address.city.trim().length === 0) {
      issues.push({ field: `${prefix}.city`, code: 'REQUIRED', message: 'City is required.' });
    }
    if (!address.stateOrProvince || address.stateOrProvince.trim().length === 0) {
      issues.push({ field: `${prefix}.stateOrProvince`, code: 'REQUIRED', message: 'State or province is required.' });
    }
    if (!address.postalCode || address.postalCode.trim().length === 0) {
      issues.push({ field: `${prefix}.postalCode`, code: 'REQUIRED', message: 'Postal code is required.' });
    }
    if (!address.countryCode || address.countryCode.length !== 2) {
      issues.push({ field: `${prefix}.countryCode`, code: 'INVALID_FORMAT', message: 'Country code must be 2-letter ISO code.' });
    }
  }
}
