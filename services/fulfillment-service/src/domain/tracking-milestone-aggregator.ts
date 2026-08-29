import { FulfillmentStatus, CarrierCode } from '@novacommerce/core-types';

export interface TrackingMilestone {
  timestamp: Date;
  status: FulfillmentStatus;
  description: string;
  locationCity?: string;
  locationState?: string;
  locationCountry?: string;
}

export class TrackingMilestoneAggregator {
  public static sortAndDeduplicate(milestones: TrackingMilestone[]): TrackingMilestone[] {
    const sorted = [...milestones].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

    const deduplicated: TrackingMilestone[] = [];
    for (const m of sorted) {
      const isDuplicate = deduplicated.some(
        d => d.status === m.status && Math.abs(new Date(d.timestamp).getTime() - new Date(m.timestamp).getTime()) < 60000
      );
      if (!isDuplicate) {
        deduplicated.push(m);
      }
    }

    return deduplicated;
  }
}
