import { OrganizationService } from '../src/services/organization.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('Organization Service Suite', () => {
  const logger = Logger.create('test');
  const service = new OrganizationService(logger);

  it('should create organization with owner membership', async () => {
    const org = await service.createOrganization('Acme Corp', 'usr-owner-1', 'billing@acme.com');
    expect(org.id).toBeDefined();
    expect(org.slug).toBe('acme-corp');

    const members = await service.getOrgMembers(org.id);
    expect(members.length).toBe(1);
    expect(members[0].role).toBe('OWNER');
  });
});
