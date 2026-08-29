import { ClickstreamEventPayload, ApiResponse } from '@novacommerce/core-types';

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
