import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_large_scale_enterprise_data():
    print("Generating comprehensive enterprise business rules and data modules...")

    # =========================================================================
    # 1. 50-State US Tax Matrix with Local Jurisdictions
    # =========================================================================
    us_tax_states_code = """export interface StateTaxRateRecord {
  stateCode: string;
  stateName: string;
  stateBaseRatePercent: number;
  averageLocalRatePercent: number;
  combinedRatePercent: number;
  taxableServices: boolean;
  taxableShipping: boolean;
  economicNexusSalesThresholdCents: number;
  economicNexusTransactionThreshold: number;
}

export const US_STATE_TAX_MATRIX: Record<string, StateTaxRateRecord> = {
"""
    states_data = [
        ("AL", "Alabama", 4.00, 5.24, 9.24, False, True, 25000000, 0),
        ("AK", "Alaska", 0.00, 1.76, 1.76, False, False, 10000000, 200),
        ("AZ", "Arizona", 5.60, 2.77, 8.37, True, False, 10000000, 0),
        ("AR", "Arkansas", 6.50, 2.93, 9.43, False, True, 10000000, 200),
        ("CA", "California", 7.25, 1.57, 8.82, False, False, 50000000, 0),
        ("CO", "Colorado", 2.90, 4.87, 7.77, False, True, 10000000, 0),
        ("CT", "Connecticut", 6.35, 0.00, 6.35, True, True, 10000000, 200),
        ("DE", "Delaware", 0.00, 0.00, 0.00, False, False, 0, 0),
        ("FL", "Florida", 6.00, 1.02, 7.02, False, False, 10000000, 0),
        ("GA", "Georgia", 4.00, 3.35, 7.35, False, True, 10000000, 200),
        ("HI", "Hawaii", 4.00, 0.44, 4.44, True, True, 10000000, 200),
        ("ID", "Idaho", 6.00, 0.03, 6.03, False, False, 10000000, 0),
        ("IL", "Illinois", 6.25, 2.56, 8.81, False, True, 10000000, 200),
        ("IN", "Indiana", 7.00, 0.00, 7.00, False, True, 10000000, 200),
        ("IA", "Iowa", 6.00, 0.94, 6.94, True, True, 10000000, 0),
        ("KS", "Kansas", 6.50, 2.19, 8.69, False, True, 10000000, 0),
        ("KY", "Kentucky", 6.00, 0.00, 6.00, False, True, 10000000, 200),
        ("LA", "Louisiana", 4.45, 5.10, 9.55, False, False, 10000000, 200),
        ("ME", "Maine", 5.50, 0.00, 5.50, False, False, 10000000, 200),
        ("MD", "Maryland", 6.00, 0.00, 6.00, False, False, 10000000, 200),
        ("MA", "Massachusetts", 6.25, 0.00, 6.25, False, False, 10000000, 0),
        ("MI", "Michigan", 6.00, 0.00, 6.00, False, True, 10000000, 200),
        ("MN", "Minnesota", 6.875, 0.61, 7.49, False, True, 10000000, 200),
        ("MS", "Mississippi", 7.00, 0.07, 7.07, False, True, 25000000, 0),
        ("MO", "Missouri", 4.225, 4.07, 8.29, False, False, 10000000, 0),
        ("MT", "Montana", 0.00, 0.00, 0.00, False, False, 0, 0),
        ("NE", "Nebraska", 5.50, 1.44, 6.94, False, True, 10000000, 200),
        ("NV", "Nevada", 6.85, 1.38, 8.23, False, False, 10000000, 200),
        ("NH", "New Hampshire", 0.00, 0.00, 0.00, False, False, 0, 0),
        ("NJ", "New Jersey", 6.625, 0.00, 6.625, False, True, 10000000, 200),
        ("NM", "New Mexico", 5.00, 2.72, 7.72, True, True, 10000000, 0),
        ("NY", "New York", 4.00, 4.52, 8.52, False, True, 50000000, 100),
        ("NC", "North Carolina", 4.75, 2.25, 7.00, False, True, 10000000, 200),
        ("ND", "North Dakota", 5.00, 1.96, 6.96, False, True, 10000000, 0),
        ("OH", "Ohio", 5.75, 1.49, 7.24, False, True, 10000000, 200),
        ("OK", "Oklahoma", 4.50, 4.47, 8.97, False, False, 10000000, 0),
        ("OR", "Oregon", 0.00, 0.00, 0.00, False, False, 0, 0),
        ("PA", "Pennsylvania", 6.00, 0.34, 6.34, False, False, 10000000, 0),
        ("RI", "Rhode Island", 7.00, 0.00, 7.00, False, True, 10000000, 200),
        ("SC", "South Carolina", 6.00, 1.44, 7.44, False, True, 10000000, 0),
        ("SD", "South Dakota", 4.50, 1.90, 6.40, True, True, 10000000, 200),
        ("TN", "Tennessee", 7.00, 2.55, 9.55, False, True, 10000000, 0),
        ("TX", "Texas", 6.25, 1.95, 8.20, True, True, 50000000, 0),
        ("UT", "Utah", 6.10, 1.09, 7.19, True, True, 10000000, 200),
        ("VT", "Vermont", 6.00, 0.24, 6.24, False, True, 10000000, 200),
        ("VA", "Virginia", 5.30, 0.45, 5.75, False, False, 10000000, 200),
        ("WA", "Washington", 6.50, 2.79, 9.29, True, True, 10000000, 0),
        ("WV", "West Virginia", 6.00, 0.55, 6.55, False, True, 10000000, 200),
        ("WI", "Wisconsin", 5.00, 0.43, 5.43, False, True, 10000000, 0),
        ("WY", "Wyoming", 4.00, 1.36, 5.36, False, True, 10000000, 200),
        ("DC", "District of Columbia", 6.00, 0.00, 6.00, True, True, 10000000, 200)
    ]
    for st, name, base, local, comb, serv, ship, sl_thresh, tx_thresh in states_data:
        us_tax_states_code += f"  {st}: {{ stateCode: '{st}', stateName: '{name}', stateBaseRatePercent: {base}, averageLocalRatePercent: {local}, combinedRatePercent: {comb}, taxableServices: {str(serv).lower()}, taxableShipping: {str(ship).lower()}, economicNexusSalesThresholdCents: {sl_thresh}, economicNexusTransactionThreshold: {tx_thresh} }},\n"
    us_tax_states_code += "};\n\n"
    us_tax_states_code += """export class ComprehensiveTaxEngine {
  public static calculateSalesTax(stateCode: string, taxableAmountCents: number, shippingFeeCents: number = 0): { taxAmountCents: number; ratePercent: number; stateBaseCents: number; localJurisdictionCents: number } {
    const rule = US_STATE_TAX_MATRIX[stateCode.toUpperCase()];
    if (!rule) {
      return { taxAmountCents: 0, ratePercent: 0, stateBaseCents: 0, localJurisdictionCents: 0 };
    }

    const eligibleBase = taxableAmountCents + (rule.taxableShipping ? shippingFeeCents : 0);
    const stateBaseCents = Math.round((eligibleBase * rule.stateBaseRatePercent) / 100);
    const localJurisdictionCents = Math.round((eligibleBase * rule.averageLocalRatePercent) / 100);
    const totalTax = stateBaseCents + localJurisdictionCents;

    return {
      taxAmountCents: totalTax,
      ratePercent: rule.combinedRatePercent,
      stateBaseCents,
      localJurisdictionCents
    };
  }
}
"""
    write_file("services/order-service/src/domain/us-tax-jurisdiction-matrix.ts", us_tax_states_code)

    # =========================================================================
    # 2. European Union VAT Rates Matrix
    # =========================================================================
    eu_vat_code = """export interface EuVatCountryRate {
  countryCode: string;
  countryName: string;
  standardRatePercent: number;
  reducedRatePercent: number;
  superReducedRatePercent?: number;
  digitalServicesRatePercent: number;
  isEuMember: boolean;
}

export const EU_VAT_COUNTRY_RATES: Record<string, EuVatCountryRate> = {
"""
    eu_countries = [
        ("AT", "Austria", 20.0, 10.0, 20.0),
        ("BE", "Belgium", 21.0, 12.0, 21.0),
        ("BG", "Bulgaria", 20.0, 9.0, 20.0),
        ("HR", "Croatia", 25.0, 13.0, 25.0),
        ("CY", "Cyprus", 19.0, 9.0, 19.0),
        ("CZ", "Czech Republic", 21.0, 12.0, 21.0),
        ("DK", "Denmark", 25.0, 0.0, 25.0),
        ("EE", "Estonia", 22.0, 9.0, 22.0),
        ("FI", "Finland", 24.0, 14.0, 24.0),
        ("FR", "France", 20.0, 10.0, 20.0),
        ("DE", "Germany", 19.0, 7.0, 19.0),
        ("GR", "Greece", 24.0, 13.0, 24.0),
        ("HU", "Hungary", 27.0, 18.0, 27.0),
        ("IE", "Ireland", 23.0, 13.5, 23.0),
        ("IT", "Italy", 22.0, 10.0, 22.0),
        ("LV", "Latvia", 21.0, 12.0, 21.0),
        ("LT", "Lithuania", 21.0, 9.0, 21.0),
        ("LU", "Luxembourg", 17.0, 14.0, 17.0),
        ("MT", "Malta", 18.0, 7.0, 18.0),
        ("NL", "Netherlands", 21.0, 9.0, 21.0),
        ("PL", "Poland", 23.0, 8.0, 23.0),
        ("PT", "Portugal", 23.0, 13.0, 23.0),
        ("RO", "Romania", 19.0, 9.0, 19.0),
        ("SK", "Slovakia", 20.0, 10.0, 20.0),
        ("SI", "Slovenia", 22.0, 9.5, 22.0),
        ("ES", "Spain", 21.0, 10.0, 21.0),
        ("SE", "Sweden", 25.0, 12.0, 25.0),
        ("GB", "United Kingdom (Post-Brexit)", 20.0, 5.0, 20.0),
        ("CH", "Switzerland", 8.1, 2.6, 8.1),
        ("NO", "Norway", 25.0, 15.0, 25.0)
    ]
    for c_code, c_name, std, red, digi in eu_countries:
        eu_vat_code += f"  {c_code}: {{ countryCode: '{c_code}', countryName: '{c_name}', standardRatePercent: {std}, reducedRatePercent: {red}, digitalServicesRatePercent: {digi}, isEuMember: true }},\n"
    eu_vat_code += "};\n\n"
    eu_vat_code += """export class EuVatCalculator {
  public static calculateVat(countryCode: string, amountCents: number, isB2bWithValidVatId: boolean = false): { vatAmountCents: number; ratePercent: number; isReverseChargeApplied: boolean } {
    if (isB2bWithValidVatId) {
      return { vatAmountCents: 0, ratePercent: 0, isReverseChargeApplied: true };
    }

    const country = EU_VAT_COUNTRY_RATES[countryCode.toUpperCase()];
    if (!country) {
      return { vatAmountCents: 0, ratePercent: 0, isReverseChargeApplied: false };
    }

    const vat = Math.round((amountCents * country.standardRatePercent) / 100);
    return {
      vatAmountCents: vat,
      ratePercent: country.standardRatePercent,
      isReverseChargeApplied: false
    };
  }
}
"""
    write_file("services/order-service/src/domain/eu-vat-matrix.ts", eu_vat_code)

    # =========================================================================
    # 3. Chart of Accounts Matrix (GAAP / IFRS Full Master Table)
    # =========================================================================
    coa_code = """export interface GlAccountRecord {
  accountNumber: string;
  accountName: string;
  accountCategory: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'COST_OF_GOODS' | 'OPERATING_EXPENSE' | 'OTHER_INCOME_EXPENSE';
  normalBalance: 'DEBIT' | 'CREDIT';
  description: string;
  isReconciliationRequired: boolean;
}

export const MASTER_CHART_OF_ACCOUNTS: GlAccountRecord[] = [
"""
    gl_accounts = [
        # Assets (1000 - 1999)
        ("101000", "Operating Cash - Main Clearing", "ASSET", "DEBIT", "Primary operating bank account for settlement clearing", True),
        ("101010", "Stripe Gateway Clearing Escrow", "ASSET", "DEBIT", "In-transit funds from Stripe gateway captures", True),
        ("101020", "PayPal Settlement Clearing Escrow", "ASSET", "DEBIT", "In-transit funds from PayPal express checkout captures", True),
        ("101030", "Apple Pay / Google Pay Merchant Clearing", "ASSET", "DEBIT", "In-transit funds from digital wallet captures", True),
        ("102000", "Trade Accounts Receivable - B2B Corporate", "ASSET", "DEBIT", "Invoiced credit accounts due from enterprise clients", True),
        ("102090", "Allowance for Doubtful Accounts (Contra)", "ASSET", "CREDIT", "Estimated uncollectible accounts receivable", True),
        ("105000", "Inventory - Finished Goods (Warehouses)", "ASSET", "DEBIT", "Available-to-promise inventory valued at standard cost", True),
        ("105010", "Inventory - In-Transit Freight", "ASSET", "DEBIT", "Inventory transfers between distribution centers", True),
        ("105090", "Inventory Reserve for Obsolescence & Shrinkage", "ASSET", "CREDIT", "Contra inventory account for cycle count discrepancies", True),
        ("108000", "Prepaid Carrier Freight & Postage", "ASSET", "DEBIT", "Prepaid postage meter and FedEx/UPS bulk account credits", True),

        # Liabilities (2000 - 2999)
        ("201000", "Trade Accounts Payable - Hardware Vendors", "LIABILITY", "CREDIT", "Vendor bills due for inventory purchases", True),
        ("201010", "Carrier Freight Payable - Logistics", "LIABILITY", "CREDIT", "Outstanding shipping carrier invoices", True),
        ("202000", "Sales & Use Tax Payable - United States", "LIABILITY", "CREDIT", "Collected sales taxes due to state tax authorities", True),
        ("202010", "Value Added Tax (VAT) Payable - European Union", "LIABILITY", "CREDIT", "Collected VAT due to EU tax administrations", True),
        ("203000", "Unearned Revenue - Customer Gift Cards", "LIABILITY", "CREDIT", "Outstanding customer store credits and gift cards", True),
        ("204000", "Accrued Customer Refunds & Returns", "LIABILITY", "CREDIT", "Estimated pending RMA refund payouts", True),
        ("205000", "Marketplace Seller Escrow Payable", "LIABILITY", "CREDIT", "Held funds pending seller delivery confirmation", True),

        # Equity (3000 - 3999)
        ("301000", "Common Stock Capital", "EQUITY", "CREDIT", "Par value of issued common equity shares", False),
        ("302000", "Additional Paid-In Capital (APIC)", "EQUITY", "CREDIT", "Capital contributions in excess of par value", False),
        ("303000", "Retained Earnings - Cumulative", "EQUITY", "CREDIT", "Cumulative net income retained in the business", False),

        # Revenue (4000 - 4999)
        ("401000", "Gross Sales Revenue - Enterprise Hardware", "REVENUE", "CREDIT", "Gross sales value from servers, laptops, and networking gear", False),
        ("402000", "Shipping & Handling Fee Income", "REVENUE", "CREDIT", "Customer-paid delivery and freight fees", False),
        ("403000", "Marketplace Platform Commission Fee Income", "REVENUE", "CREDIT", "Transaction take-rate fees charged to 3rd party sellers", False),
        ("409000", "Customer Sales Discounts & Promo Coupons (Contra)", "REVENUE", "DEBIT", "Coupons and promotional discounts deducted from sales", False),
        ("409010", "Customer Returns & Allowances (Contra)", "REVENUE", "DEBIT", "Refunds and price concessions granted on returned goods", False),

        # Cost of Goods Sold (5000 - 5999)
        ("501000", "Cost of Goods Sold - Hardware Products", "COST_OF_GOODS", "DEBIT", "Cost of inventory sold during the accounting period", False),
        ("502000", "Carrier Outbound Freight Shipping Expense", "COST_OF_GOODS", "DEBIT", "Direct courier shipping expenses paid to FedEx, UPS, DHL", False),
        ("503000", "Warehouse Packaging & Supplies Expense", "COST_OF_GOODS", "DEBIT", "Boxes, dunnage, thermal labels, and pallets", False),
        ("504000", "Inventory Scrap & Write-Down Expense", "COST_OF_GOODS", "DEBIT", "Damaged goods discarded during RMA inspection", False),

        # Operating Expenses (6000 - 6999)
        ("601000", "Payment Gateway Merchant Processing Fees", "OPERATING_EXPENSE", "DEBIT", "Interchange fees, Stripe 2.9% + 30c, and bank fees", False),
        ("602000", "Cloud Computing & Data Infrastructure", "OPERATING_EXPENSE", "DEBIT", "AWS, GCP, Kubernetes hosting, and CDN costs", False),
        ("603000", "Customer Support & Chargeback Loss Expense", "OPERATING_EXPENSE", "DEBIT", "Dispute fees and unrecoverable fraudulent chargebacks", False)
    ]
    for num, name, cat, norm, desc, recon in gl_accounts:
        coa_code += f"  {{ accountNumber: '{num}', accountName: '{name}', accountCategory: '{cat}', normalBalance: '{norm}', description: '{desc}', isReconciliationRequired: {str(recon).lower()} }},\n"
    coa_code += "];\n\n"
    coa_code += """export class GeneralLedgerChartOfAccounts {
  public static getAccount(accountNumber: string): GlAccountRecord | undefined {
    return MASTER_CHART_OF_ACCOUNTS.find(a => a.accountNumber === accountNumber);
  }

  public static getAccountsByCategory(category: GlAccountRecord['accountCategory']): GlAccountRecord[] {
    return MASTER_CHART_OF_ACCOUNTS.filter(a => a.accountCategory === category);
  }
}
"""
    write_file("services/payment-service/src/domain/chart-of-accounts-matrix.ts", coa_code)

    print("Large scale enterprise data modules generated.")

if __name__ == "__main__":
    generate_large_scale_enterprise_data()
