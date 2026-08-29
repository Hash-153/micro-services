import { RbacPolicyEngine, Permission } from '../src/services/rbac-policy.service.js';
import { UserRole } from '@novacommerce/core-types';

describe('Auth Service: Comprehensive RBAC Permission Evaluation Suite', () => {
  it('should verify that SUPER_ADMIN possesses all permissions', () => {
    const allPermissions = Object.values(Permission);
    for (const perm of allPermissions) {
      expect(RbacPolicyEngine.hasPermission(UserRole.SUPER_ADMIN, perm)).toBe(true);
    }
  });

  it('should verify that FINANCE_ANALYST possesses ledger view but not product delete', () => {
    expect(RbacPolicyEngine.hasPermission(UserRole.FINANCE_ANALYST, Permission.LEDGER_VIEW)).toBe(true);
    expect(RbacPolicyEngine.hasPermission(UserRole.FINANCE_ANALYST, Permission.PRODUCT_DELETE)).toBe(false);
  });

  it('should verify that GUEST can only read products', () => {
    expect(RbacPolicyEngine.hasPermission(UserRole.GUEST, Permission.PRODUCT_READ)).toBe(true);
    expect(RbacPolicyEngine.hasPermission(UserRole.GUEST, Permission.ORDER_CREATE)).toBe(false);
  });
});
