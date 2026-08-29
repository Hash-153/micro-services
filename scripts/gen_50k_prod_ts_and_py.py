import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_typescript_sdk_complete():
    print("Generating comprehensive TypeScript SDK API modules...")
    pkg = "sdks/typescript/src/api"

    write_file(f"{pkg}/UserApiClient.ts", """import { UserProfileEntity, AddressEntity, OrganizationEntity, ApiResponse } from '@novacommerce/core-types';

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
""")

    write_file(f"{pkg}/NotificationApiClient.ts", """import { NotificationDispatchPayload, ApiResponse } from '@novacommerce/core-types';

export class NotificationApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async sendNotification(payload: NotificationDispatchPayload): Promise<{ messageId: string; status: string }> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/notifications/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error(`Send notification failed: ${res.statusText}`);
    const json = await res.json();
    return json.data;
  }

  public async listTemplates(): Promise<any[]> {
    const res = await fetch(`${this.baseUrl}/api/v1/notifications/templates`);
    if (!res.ok) throw new Error(`List templates failed: ${res.statusText}`);
    const json = await res.json();
    return json.data;
  }
}
""")

    write_file(f"{pkg}/AnalyticsApiClient.ts", """import { ClickstreamEventPayload, ApiResponse } from '@novacommerce/core-types';

export class AnalyticsApiClient {
  private readonly baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  public async trackEvent(payload: ClickstreamEventPayload): Promise<boolean> {
    const res = await fetch(`${this.baseUrl}/api/v1/analytics/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.ok;
  }

  public async getRevenueRollup(): Promise<any> {
    const res = await fetch(`${this.baseUrl}/api/v1/analytics/revenue-rollup`);
    if (!res.ok) throw new Error(`Get revenue rollup failed: ${res.statusText}`);
    const json = await res.json();
    return json.data;
  }
}
""")

    print("TypeScript SDK complete.")

if __name__ == "__main__":
    generate_typescript_sdk_complete()
