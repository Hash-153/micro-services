export interface TaxNexusRule {
  stateCode: string;
  stateName: string;
  hasEconomicNexus: boolean;
  annualSalesThresholdCents: number;
  annualTransactionThreshold: number;
  collectsFreightTax: boolean;
  standardVatPercent?: number;
}

export class TaxNexusEngine {
  private static readonly NEXUS_RULES: Record<string, TaxNexusRule> = {
    CA: { stateCode: 'CA', stateName: 'California', hasEconomicNexus: true, annualSalesThresholdCents: 50000000, annualTransactionThreshold: 200, collectsFreightTax: false },
    NY: { stateCode: 'NY', stateName: 'New York', hasEconomicNexus: true, annualSalesThresholdCents: 50000000, annualTransactionThreshold: 100, collectsFreightTax: true },
    TX: { stateCode: 'TX', stateName: 'Texas', hasEconomicNexus: true, annualSalesThresholdCents: 50000000, annualTransactionThreshold: 0, collectsFreightTax: true },
    FL: { stateCode: 'FL', stateName: 'Florida', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false },
    IL: { stateCode: 'IL', stateName: 'Illinois', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    PA: { stateCode: 'PA', stateName: 'Pennsylvania', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false },
    OH: { stateCode: 'OH', stateName: 'Ohio', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    GA: { stateCode: 'GA', stateName: 'Georgia', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    NC: { stateCode: 'NC', stateName: 'North Carolina', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    MI: { stateCode: 'MI', stateName: 'Michigan', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    NJ: { stateCode: 'NJ', stateName: 'New Jersey', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    VA: { stateCode: 'VA', stateName: 'Virginia', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: false },
    WA: { stateCode: 'WA', stateName: 'Washington', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: true },
    AZ: { stateCode: 'AZ', stateName: 'Arizona', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false },
    MA: { stateCode: 'MA', stateName: 'Massachusetts', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false }
  };

  public static hasNexus(stateCode: string, currentAnnualSalesCents: number, currentAnnualTransactions: number): boolean {
    const rule = this.NEXUS_RULES[stateCode.toUpperCase()];
    if (!rule || !rule.hasEconomicNexus) return false;
    return (
      currentAnnualSalesCents >= rule.annualSalesThresholdCents ||
      (rule.annualTransactionThreshold > 0 && currentAnnualTransactions >= rule.annualTransactionThreshold)
    );
  }

  public static isFreightTaxable(stateCode: string): boolean {
    const rule = this.NEXUS_RULES[stateCode.toUpperCase()];
    return rule ? rule.collectsFreightTax : false;
  }
}
