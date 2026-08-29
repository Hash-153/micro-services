export class SafetyLeadTimeBuffer {
  public static calculateBufferedLeadTime(nominalLeadTimeDays: number, supplierOnTimePercentage: number): number {
    if (supplierOnTimePercentage >= 98.0) {
      return nominalLeadTimeDays; // No extra buffer needed
    }

    if (supplierOnTimePercentage >= 90.0) {
      return nominalLeadTimeDays + 2; // +2 days buffer
    }

    if (supplierOnTimePercentage >= 80.0) {
      return nominalLeadTimeDays + 5; // +5 days buffer
    }

    return nominalLeadTimeDays + 10; // Unreliable supplier: +10 days buffer
  }
}
