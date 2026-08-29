import { UserRole } from '@novacommerce/core-types';

export enum Permission {
  // Products & Catalog
  PRODUCT_READ = 'product:read',
  PRODUCT_CREATE = 'product:create',
  PRODUCT_UPDATE = 'product:update',
  PRODUCT_DELETE = 'product:delete',

  // Orders
  ORDER_READ_OWN = 'order:read_own',
  ORDER_READ_ALL = 'order:read_all',
  ORDER_CREATE = 'order:create',
  ORDER_CANCEL = 'order:cancel',
  ORDER_REFUND = 'order:refund',

  // Inventory
  INVENTORY_READ = 'inventory:read',
  INVENTORY_ADJUST = 'inventory:adjust',
  INVENTORY_TRANSFER = 'inventory:transfer',

  // Payments & Ledger
  PAYMENT_PROCESS = 'payment:process',
  LEDGER_VIEW = 'ledger:view',
  LEDGER_EXPORT = 'ledger:export',

  // Users & IAM
  USER_READ_OWN = 'user:read_own',
  USER_READ_ALL = 'user:read_all',
  USER_MANAGE_ROLES = 'user:manage_roles',
  AUDIT_LOG_VIEW = 'audit:view'
}

export const ROLE_PERMISSION_MATRIX: Record<UserRole, Permission[]> = {
  [UserRole.SUPER_ADMIN]: Object.values(Permission),
  [UserRole.ADMIN]: [
    Permission.PRODUCT_READ, Permission.PRODUCT_CREATE, Permission.PRODUCT_UPDATE, Permission.PRODUCT_DELETE,
    Permission.ORDER_READ_ALL, Permission.ORDER_CREATE, Permission.ORDER_CANCEL, Permission.ORDER_REFUND,
    Permission.INVENTORY_READ, Permission.INVENTORY_ADJUST, Permission.INVENTORY_TRANSFER,
    Permission.PAYMENT_PROCESS, Permission.LEDGER_VIEW, Permission.LEDGER_EXPORT,
    Permission.USER_READ_ALL, Permission.USER_MANAGE_ROLES, Permission.AUDIT_LOG_VIEW
  ],
  [UserRole.OPERATIONS_MANAGER]: [
    Permission.PRODUCT_READ, Permission.PRODUCT_UPDATE,
    Permission.ORDER_READ_ALL, Permission.ORDER_CANCEL,
    Permission.INVENTORY_READ, Permission.INVENTORY_ADJUST, Permission.INVENTORY_TRANSFER
  ],
  [UserRole.INVENTORY_MANAGER]: [
    Permission.PRODUCT_READ,
    Permission.INVENTORY_READ, Permission.INVENTORY_ADJUST, Permission.INVENTORY_TRANSFER
  ],
  [UserRole.FINANCE_ANALYST]: [
    Permission.ORDER_READ_ALL,
    Permission.LEDGER_VIEW, Permission.LEDGER_EXPORT,
    Permission.PAYMENT_PROCESS, Permission.AUDIT_LOG_VIEW
  ],
  [UserRole.SUPPORT_AGENT]: [
    Permission.PRODUCT_READ,
    Permission.ORDER_READ_ALL, Permission.ORDER_CANCEL,
    Permission.USER_READ_ALL
  ],
  [UserRole.CUSTOMER]: [
    Permission.PRODUCT_READ,
    Permission.ORDER_READ_OWN, Permission.ORDER_CREATE,
    Permission.USER_READ_OWN
  ],
  [UserRole.GUEST]: [
    Permission.PRODUCT_READ
  ],
  [UserRole.SYSTEM_INTERNAL]: Object.values(Permission)
};

export class RbacPolicyEngine {
  public static hasPermission(role: UserRole, permission: Permission): boolean {
    const permissions = ROLE_PERMISSION_MATRIX[role] || [];
    return permissions.includes(permission);
  }

  public static hasAllPermissions(role: UserRole, permissions: Permission[]): boolean {
    return permissions.every(p => this.hasPermission(role, p));
  }

  public static hasAnyPermission(role: UserRole, permissions: Permission[]): boolean {
    return permissions.some(p => this.hasPermission(role, p));
  }
}
