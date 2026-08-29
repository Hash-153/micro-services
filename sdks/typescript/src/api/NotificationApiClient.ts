import { NotificationDispatchPayload, ApiResponse } from '@novacommerce/core-types';

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
