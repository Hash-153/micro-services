export interface SettlementSchedule {
  merchantId: string;
  payoutFrequency: 'DAILY_ROLLING' | 'WEEKLY_FRIDAY' | 'MONTHLY_FIRST';
  rollingDaysDelay: number;
  nextPayoutDate: Date;
  cutoffTimeUtc: string;
}

export class MerchantSettlementScheduler {
  public static calculateNextPayout(schedule: SettlementSchedule, currentDate: Date = new Date()): Date {
    const nextDate = new Date(currentDate);

    if (schedule.payoutFrequency === 'DAILY_ROLLING') {
      nextDate.setDate(nextDate.getDate() + schedule.rollingDaysDelay);
      // If weekend, push to Monday
      if (nextDate.getDay() === 6) nextDate.setDate(nextDate.getDate() + 2);
      if (nextDate.getDay() === 0) nextDate.setDate(nextDate.getDate() + 1);
    } else if (schedule.payoutFrequency === 'WEEKLY_FRIDAY') {
      const daysUntilFriday = (5 - nextDate.getDay() + 7) % 7 || 7;
      nextDate.setDate(nextDate.getDate() + daysUntilFriday);
    } else if (schedule.payoutFrequency === 'MONTHLY_FIRST') {
      nextDate.setMonth(nextDate.getMonth() + 1);
      nextDate.setDate(1);
    }

    return nextDate;
  }
}
