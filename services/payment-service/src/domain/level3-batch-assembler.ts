import { Level3ProcessingPayload } from './level3-card-data-builder.js';

export interface Level3BatchSubmission {
  batchId: string;
  merchantId: string;
  totalRecords: number;
  totalFreightCents: number;
  totalDutyCents: number;
  records: Level3ProcessingPayload[];
}

export class Level3BatchAssembler {
  public static assembleBatch(merchantId: string, records: Level3ProcessingPayload[]): Level3BatchSubmission {
    const totalFreight = records.reduce((acc, r) => acc + r.freightAmountCents, 0);
    const totalDuty = records.reduce((acc, r) => acc + r.dutyAmountCents, 0);

    return {
      batchId: `L3-BATCH-${Date.now().toString(36).toUpperCase()}`,
      merchantId,
      totalRecords: records.length,
      totalFreightCents: totalFreight,
      totalDutyCents: totalDuty,
      records
    };
  }
}
