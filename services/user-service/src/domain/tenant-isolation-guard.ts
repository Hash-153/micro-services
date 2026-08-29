export class TenantIsolationGuard {
  public static enforceOrgAccess(requestedOrgId: string, userOrgId?: string, isSuperAdmin: boolean = false): void {
    if (isSuperAdmin) return; // Super admins have global access

    if (!userOrgId || userOrgId !== requestedOrgId) {
      throw new Error(`Tenant access violation: user in organization '${userOrgId || 'NONE'}' cannot access resources in organization '${requestedOrgId}'`);
    }
  }
}
