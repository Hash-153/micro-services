export interface SubLedgerAccount {
  glCode: string;
  accountName: string;
  category: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'EXPENSE';
  parentGlCode?: string;
  departmentCode: string;
  taxJurisdictionCode?: string;
}

export class SubLedgerHierarchy {
  private static readonly ACCOUNTS: SubLedgerAccount[] = [
    // 1000 - Assets
    { glCode: '1010-00', accountName: 'Operating Cash - Main Clearing', category: 'ASSET', departmentCode: 'TREASURY' },
    { glCode: '1010-01', accountName: 'Stripe Settlement Escrow', category: 'ASSET', departmentCode: 'PAYMENTS' },
    { glCode: '1010-02', accountName: 'PayPal Settlement Escrow', category: 'ASSET', departmentCode: 'PAYMENTS' },
    { glCode: '1020-00', accountName: 'Accounts Receivable - Corporate B2B', category: 'ASSET', departmentCode: 'FINANCE' },
    { glCode: '1050-00', accountName: 'Finished Goods Inventory Stock', category: 'ASSET', departmentCode: 'WAREHOUSE' },

    // 2000 - Liabilities
    { glCode: '2010-00', accountName: 'Accounts Payable - Courier Logistics', category: 'LIABILITY', departmentCode: 'LOGISTICS' },
    { glCode: '2020-CA', accountName: 'California State Sales Tax Payable', category: 'LIABILITY', departmentCode: 'TAX', taxJurisdictionCode: 'CA' },
    { glCode: '2020-NY', accountName: 'New York State Sales Tax Payable', category: 'LIABILITY', departmentCode: 'TAX', taxJurisdictionCode: 'NY' },
    { glCode: '2020-TX', accountName: 'Texas State Sales Tax Payable', category: 'LIABILITY', departmentCode: 'TAX', taxJurisdictionCode: 'TX' },
    { glCode: '2030-00', accountName: 'Customer Store Credit & Gift Card Liability', category: 'LIABILITY', departmentCode: 'FINANCE' },

    // 4000 - Revenue
    { glCode: '4010-00', accountName: 'Hardware Product Sales Revenue', category: 'REVENUE', departmentCode: 'COMMERCE' },
    { glCode: '4020-00', accountName: 'Freight & Delivery Income', category: 'REVENUE', departmentCode: 'LOGISTICS' },
    { glCode: '4090-00', accountName: 'Customer Promotional Discounts (Contra)', category: 'REVENUE', departmentCode: 'MARKETING' },

    // 5000 - Expenses
    { glCode: '5010-00', accountName: 'Cost of Goods Sold - Hardware', category: 'EXPENSE', departmentCode: 'COMMERCE' },
    { glCode: '5020-00', accountName: 'Carrier Shipping Freight Expense', category: 'EXPENSE', departmentCode: 'LOGISTICS' },
    { glCode: '5030-00', accountName: 'Payment Interchange & Processing Fees', category: 'EXPENSE', departmentCode: 'PAYMENTS' }
  ];

  public static getAccount(glCode: string): SubLedgerAccount | undefined {
    return this.ACCOUNTS.find(a => a.glCode === glCode);
  }

  public static getTaxPayableAccount(stateCode: string): SubLedgerAccount {
    const found = this.ACCOUNTS.find(a => a.taxJurisdictionCode === stateCode.toUpperCase());
    return found || {
      glCode: `2020-${stateCode.toUpperCase()}`,
      accountName: `${stateCode.toUpperCase()} Sales Tax Payable`,
      category: 'LIABILITY',
      departmentCode: 'TAX',
      taxJurisdictionCode: stateCode.toUpperCase()
    };
  }
}
