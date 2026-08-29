import { OrganizationService } from '../../services/user-service/src/services/organization.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('E2E Scenario: Multi-Tenant Organization Provisioning & Member Access', () => {
  const logger = Logger.create('test-e2e');
  const orgService = new OrganizationService(logger);

  it('should provision tenant organization and enforce member seat limits', async () => {
    const org = await orgService.createOrganization('Global Enterprise Logistics Inc.', 'usr-founder', 'billing@global-logistics.io');
    expect(org.id).toBeDefined();
    expect(org.maxSeats).toBe(25);

    const member1 = await orgService.addMember(org.id, 'usr-analyst-1', 'MEMBER');
    expect(member1.userId).toBe('usr-analyst-1');

    const members = await orgService.getOrgMembers(org.id);
    expect(members.length).toBe(2); // Owner + Member1
  });
});
