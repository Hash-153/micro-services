import { RbacPolicyEngine, Permission } from '../src/services/rbac-policy.service.js';
import { UserRole } from '@novacommerce/core-types';

describe('RBAC Policy Suite', () => {
  it('should grant SUPER_ADMIN all permissions', () => {
    expect(RbacPolicyEngine.hasPermission(UserRole.SUPER_ADMIN, Permission.PRODUCT_DELETE)).toBe(true);
    expect(RbacPolicyEngine.hasPermission(UserRole.SUPER_ADMIN, Permission.LEDGER_VIEW)).toBe(true);
  });

  it('should restrict CUSTOMER to own resources only', () => {
    expect(RbacPolicyEngine.hasPermission(UserRole.CUSTOMER, Permission.PRODUCT_READ)).toBe(true);
    expect(RbacPolicyEngine.hasPermission(UserRole.CUSTOMER, Permission.PRODUCT_DELETE)).toBe(false);
    expect(RbacPolicyEngine.hasPermission(UserRole.CUSTOMER, Permission.LEDGER_VIEW)).toBe(false);
  });
});
