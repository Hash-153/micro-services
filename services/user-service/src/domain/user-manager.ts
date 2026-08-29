import { UserEntity, UserProfileEntity, AddressEntity, OrganizationEntity, OrganizationMemberEntity } from '@novacommerce/core-types';

export interface CreateUserRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phoneNumber?: string;
  organizationId?: string;
}

export interface UpdateUserRequest {
  firstName?: string;
  lastName?: string;
  phoneNumber?: string;
  avatarUrl?: string;
  timezone?: string;
  locale?: string;
}

export class UserManager {
  private users: Map<string, UserEntity> = new Map();
  private profiles: Map<string, UserProfileEntity> = new Map();
  private addresses: Map<string, AddressEntity> = new Map();
  private organizations: Map<string, OrganizationEntity> = new Map();
  private organizationMembers: Map<string, OrganizationMemberEntity> = new Map();

  public async createUser(request: CreateUserRequest): Promise<UserEntity> {
    // Check if user already exists
    const existing = Array.from(this.users.values()).find(u => u.email === request.email);
    if (existing) {
      throw new Error('User with this email already exists');
    }

    const passwordHash = await this.hashPassword(request.password);

    const user: UserEntity = {
      id: `user-${Date.now()}`,
      email: request.email,
      passwordHash,
      role: 'CUSTOMER',
      status: 'ACTIVE',
      kycStatus: 'NOT_VERIFIED',
      organizationId: request.organizationId || null,
      isMfaEnabled: false,
      failedLoginAttempts: 0,
      passwordChangedAt: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.users.set(user.id, user);

    // Create user profile
    const profile: UserProfileEntity = {
      id: `profile-${Date.now()}`,
      userId: user.id,
      firstName: request.firstName,
      lastName: request.lastName,
      phoneNumber: request.phoneNumber || null,
      avatarUrl: null,
      timezone: 'UTC',
      locale: 'en-US',
      preferences: {
        marketingEmails: true,
        orderSmsNotifications: true,
        twoFactorRequiredForOrders: false,
        preferredCurrency: 'USD',
        theme: 'system'
      },
      metadata: {},
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.profiles.set(profile.id, profile);

    return user;
  }

  public async getUserById(userId: string): Promise<UserEntity | null> {
    return this.users.get(userId) || null;
  }

  public async getUserByEmail(email: string): Promise<UserEntity | null> {
    return Array.from(this.users.values()).find(u => u.email === email) || null;
  }

  public async getUserProfile(userId: string): Promise<UserProfileEntity | null> {
    return Array.from(this.profiles.values()).find(p => p.userId === userId) || null;
  }

  public async updateUser(userId: string, request: UpdateUserRequest): Promise<UserProfileEntity> {
    const profile = Array.from(this.profiles.values()).find(p => p.userId === userId);
    if (!profile) {
      throw new Error('User profile not found');
    }

    if (request.firstName !== undefined) profile.firstName = request.firstName;
    if (request.lastName !== undefined) profile.lastName = request.lastName;
    if (request.phoneNumber !== undefined) profile.phoneNumber = request.phoneNumber;
    if (request.avatarUrl !== undefined) profile.avatarUrl = request.avatarUrl;
    if (request.timezone !== undefined) profile.timezone = request.timezone;
    if (request.locale !== undefined) profile.locale = request.locale;

    profile.updatedAt = new Date();
    this.profiles.set(profile.id, profile);

    return profile;
  }

  public async addAddress(userId: string, address: Omit<AddressEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<AddressEntity> {
    const newAddress: AddressEntity = {
      ...address,
      id: `addr-${Date.now()}`,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.addresses.set(newAddress.id, newAddress);

    return newAddress;
  }

  public async getUserAddresses(userId: string): Promise<AddressEntity[]> {
    return Array.from(this.addresses.values()).filter(a => a.userId === userId);
  }

  public async updateAddress(addressId: string, updates: Partial<AddressEntity>): Promise<AddressEntity> {
    const address = this.addresses.get(addressId);
    if (!address) {
      throw new Error('Address not found');
    }

    Object.assign(address, updates);
    address.updatedAt = new Date();
    this.addresses.set(addressId, address);

    return address;
  }

  public async deleteAddress(addressId: string): Promise<boolean> {
    return this.addresses.delete(addressId);
  }

  public async createOrganization(name: string, billingEmail: string, userId: string): Promise<OrganizationEntity> {
    const slug = this.generateSlug(name);

    const organization: OrganizationEntity = {
      id: `org-${Date.now()}`,
      name,
      slug,
      billingEmail,
      tier: 'FREE',
      maxSeats: 5,
      isActive: true,
      settings: {},
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.organizations.set(organization.id, organization);

    // Add creator as owner
    const member: OrganizationMemberEntity = {
      id: `member-${Date.now()}`,
      organizationId: organization.id,
      userId,
      role: 'OWNER',
      joinedAt: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.organizationMembers.set(member.id, member);

    // Update user with organization
    const user = this.users.get(userId);
    if (user) {
      user.organizationId = organization.id;
      user.updatedAt = new Date();
      this.users.set(userId, user);
    }

    return organization;
  }

  public async getOrganizationById(orgId: string): Promise<OrganizationEntity | null> {
    return this.organizations.get(orgId) || null;
  }

  public async getOrganizationBySlug(slug: string): Promise<OrganizationEntity | null> {
    return Array.from(this.organizations.values()).find(o => o.slug === slug) || null;
  }

  public async addOrganizationMember(orgId: string, userId: string, role: 'ADMIN' | 'MEMBER' | 'BILLING_MANAGER' | 'READ_ONLY'): Promise<OrganizationMemberEntity> {
    const member: OrganizationMemberEntity = {
      id: `member-${Date.now()}`,
      organizationId: orgId,
      userId,
      role,
      joinedAt: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.organizationMembers.set(member.id, member);

    return member;
  }

  public async getOrganizationMembers(orgId: string): Promise<OrganizationMemberEntity[]> {
    return Array.from(this.organizationMembers.values()).filter(m => m.organizationId === orgId);
  }

  public async updateOrganizationMember(memberId: string, role: 'ADMIN' | 'MEMBER' | 'BILLING_MANAGER' | 'READ_ONLY'): Promise<OrganizationMemberEntity> {
    const member = this.organizationMembers.get(memberId);
    if (!member) {
      throw new Error('Organization member not found');
    }

    member.role = role;
    member.updatedAt = new Date();
    this.organizationMembers.set(memberId, member);

    return member;
  }

  public async removeOrganizationMember(memberId: string): Promise<boolean> {
    return this.organizationMembers.delete(memberId);
  }

  private async hashPassword(password: string): Promise<string> {
    // In production, use proper password hashing (bcrypt, argon2, etc.)
    // This is a placeholder implementation
    const hash = password.split('').reduce((acc, char) => {
      return ((acc << 5) - acc) + char.charCodeAt(0);
    }, 0);
    return `HASH_${Math.abs(hash).toString(16)}`;
  }

  private generateSlug(name: string): string {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '')
      .substring(0, 50);
  }

  public async verifyPassword(email: string, password: string): Promise<UserEntity | null> {
    const user = await this.getUserByEmail(email);
    if (!user) {
      return null;
    }

    const passwordHash = await this.hashPassword(password);
    if (user.passwordHash !== passwordHash) {
      user.failedLoginAttempts++;
      if (user.failedLoginAttempts >= 5) {
        user.lockedUntil = new Date(Date.now() + 15 * 60 * 1000); // Lock for 15 minutes
      }
      user.updatedAt = new Date();
      this.users.set(user.id, user);
      return null;
    }

    // Reset failed attempts on successful login
    user.failedLoginAttempts = 0;
    user.lastLoginAt = new Date();
    user.updatedAt = new Date();
    this.users.set(user.id, user);

    return user;
  }

  public async changePassword(userId: string, oldPassword: string, newPassword: string): Promise<boolean> {
    const user = this.users.get(userId);
    if (!user) {
      return false;
    }

    const oldPasswordHash = await this.hashPassword(oldPassword);
    if (user.passwordHash !== oldPasswordHash) {
      return false;
    }

    user.passwordHash = await this.hashPassword(newPassword);
    user.passwordChangedAt = new Date();
    user.updatedAt = new Date();
    this.users.set(userId, user);

    return true;
  }
}
