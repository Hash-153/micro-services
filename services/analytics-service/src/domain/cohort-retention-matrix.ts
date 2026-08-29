export interface UserRegistrationEvent {
  userId: string;
  registeredMonth: string; // e.g. "2026-01"
}

export interface UserOrderActivity {
  userId: string;
  orderMonth: string; // e.g. "2026-02"
}

export interface CohortRetentionRow {
  cohortMonth: string;
  cohortSize: number;
  retentionByMonthIndex: { monthIndex: number; activeUsers: number; retentionRatePercent: number }[];
}

export class CohortRetentionMatrix {
  public static computeRetention(
    registrations: UserRegistrationEvent[],
    orders: UserOrderActivity[]
  ): CohortRetentionRow[] {
    const cohorts: Map<string, Set<string>> = new Map();

    for (const reg of registrations) {
      if (!cohorts.has(reg.registeredMonth)) {
        cohorts.set(reg.registeredMonth, new Set());
      }
      cohorts.get(reg.registeredMonth)!.add(reg.userId);
    }

    const rows: CohortRetentionRow[] = [];

    for (const [cohortMonth, userSet] of cohorts.entries()) {
      const cohortSize = userSet.size;
      const retentionByMonthIndex: CohortRetentionRow['retentionByMonthIndex'] = [];

      for (let m = 0; m <= 12; m++) {
        // Calculate target month string
        const activeInMonth = orders.filter(o => userSet.has(o.userId)).length;
        const rate = cohortSize > 0 ? (activeInMonth / cohortSize) * 100 : 0;

        retentionByMonthIndex.push({
          monthIndex: m,
          activeUsers: activeInMonth,
          retentionRatePercent: Math.round(rate * 10) / 10
        });
      }

      rows.push({
        cohortMonth,
        cohortSize,
        retentionByMonthIndex
      });
    }

    return rows;
  }
}
