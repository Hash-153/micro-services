import { ILogger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

export interface OrganizationEntity {
  id: string;
  name: string;
  slug: string;
  billingEmail: string;
  tier: 'FREE' | 'PRO' | 'ENTERPRISE';
  maxSeats: number;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface OrganizationMember {
  id: string;
  organizationId: string;
  userId: string;
  role: 'OWNER' | 'ADMIN' | 'MEMBER' | 'BILLING';
  joinedAt: Date;
}

export class OrganizationService {
  private readonly orgs: Map<string, OrganizationEntity> = new Map();
  private readonly members: Map<string, OrganizationMember[]> = new Map();
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'OrganizationService' });
  }

  public async createOrganization(name: string, ownerUserId: string, billingEmail: string): Promise<OrganizationEntity> {
    const orgId = randomUUID();
    const slug = name.toLowerCase().replace(/[^a-z0-9]/g, '-');
    const org: OrganizationEntity = {
      id: orgId,
      name,
      slug,
      billingEmail,
      tier: 'PRO',
      maxSeats: 25,
      isActive: true,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.orgs.set(orgId, org);

    const ownerMember: OrganizationMember = {
      id: randomUUID(),
      organizationId: orgId,
      userId: ownerUserId,
      role: 'OWNER',
      joinedAt: new Date()
    };

    this.members.set(orgId, [ownerMember]);
    this.logger.info(`Created Organization '${name}' (${orgId}) for owner ${ownerUserId}`);
    return org;
  }

  public async addMember(orgId: string, userId: string, role: 'ADMIN' | 'MEMBER' | 'BILLING' = 'MEMBER'): Promise<OrganizationMember> {
    const org = this.orgs.get(orgId);
    if (!org) throw new Error(`Organization ${orgId} not found.`);

    const currentMembers = this.members.get(orgId) || [];
    if (currentMembers.length >= org.maxSeats) {
      throw new Error(`Organization seat limit reached (${org.maxSeats}).`);
    }

    const member: OrganizationMember = {
      id: randomUUID(),
      organizationId: orgId,
      userId,
      role,
      joinedAt: new Date()
    };

    currentMembers.push(member);
    this.members.set(orgId, currentMembers);
    return member;
  }

  public async getOrgMembers(orgId: string): Promise<OrganizationMember[]> {
    return this.members.get(orgId) || [];
  }
}
