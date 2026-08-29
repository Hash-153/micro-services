export enum EventType {
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
