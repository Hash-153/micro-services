import { UserProfileEntity, AddressEntity, OrganizationEntity, ApiResponse } from '@novacommerce/core-types';

export class UserApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async getProfile(): Promise<UserProfileEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/users/profile`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Get profile failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<UserProfileEntity>;
    return json.data;
  }

  public async updateProfile(updates: Partial<UserProfileEntity>): Promise<UserProfileEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/users/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(updates)
    });
    if (!res.ok) throw new Error(`Update profile failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<UserProfileEntity>;
    return json.data;
  }

  public async listAddresses(): Promise<AddressEntity[]> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/users/addresses`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`List addresses failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<AddressEntity[]>;
    return json.data;
  }

  public async addAddress(address: Omit<AddressEntity, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<AddressEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/users/addresses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(address)
    });
    if (!res.ok) throw new Error(`Add address failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<AddressEntity>;
    return json.data;
  }

  public async deleteAddress(addressId: string): Promise<boolean> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/users/addresses/${addressId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });
    return res.ok;
  }
}
