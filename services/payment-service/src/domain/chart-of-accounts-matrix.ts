export interface GlAccountRecord {
  accountNumber: string;
  accountName: string;
  accountCategory: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'COST_OF_GOODS' | 'OPERATING_EXPENSE' | 'OTHER_INCOME_EXPENSE';
  normalBalance: 'DEBIT' | 'CREDIT';
  description: string;
  isReconciliationRequired: boolean;
}

export const MASTER_CHART_OF_ACCOUNTS: GlAccountRecord[] = [
  { accountNumber: '101000', accountName: 'Operating Cash - Main Clearing', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'Primary operating bank account for settlement clearing', isReconciliationRequired: true },
  { accountNumber: '101010', accountName: 'Stripe Gateway Clearing Escrow', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'In-transit funds from Stripe gateway captures', isReconciliationRequired: true },
  { accountNumber: '101020', accountName: 'PayPal Settlement Clearing Escrow', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'In-transit funds from PayPal express checkout captures', isReconciliationRequired: true },
  { accountNumber: '101030', accountName: 'Apple Pay / Google Pay Merchant Clearing', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'In-transit funds from digital wallet captures', isReconciliationRequired: true },
  { accountNumber: '102000', accountName: 'Trade Accounts Receivable - B2B Corporate', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'Invoiced credit accounts due from enterprise clients', isReconciliationRequired: true },
  { accountNumber: '102090', accountName: 'Allowance for Doubtful Accounts (Contra)', accountCategory: 'ASSET', normalBalance: 'CREDIT', description: 'Estimated uncollectible accounts receivable', isReconciliationRequired: true },
  { accountNumber: '105000', accountName: 'Inventory - Finished Goods (Warehouses)', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'Available-to-promise inventory valued at standard cost', isReconciliationRequired: true },
  { accountNumber: '105010', accountName: 'Inventory - In-Transit Freight', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'Inventory transfers between distribution centers', isReconciliationRequired: true },
  { accountNumber: '105090', accountName: 'Inventory Reserve for Obsolescence & Shrinkage', accountCategory: 'ASSET', normalBalance: 'CREDIT', description: 'Contra inventory account for cycle count discrepancies', isReconciliationRequired: true },
  { accountNumber: '108000', accountName: 'Prepaid Carrier Freight & Postage', accountCategory: 'ASSET', normalBalance: 'DEBIT', description: 'Prepaid postage meter and FedEx/UPS bulk account credits', isReconciliationRequired: true },
  { accountNumber: '201000', accountName: 'Trade Accounts Payable - Hardware Vendors', accountCategory: 'LIABILITY', normalBalance: 'CREDIT', description: 'Vendor bills due for inventory purchases', isReconciliationRequired: true },
  { accountNumber: '201010', accountName: 'Carrier Freight Payable - Logistics', accountCategory: 'LIABILITY', normalBalance: 'CREDIT', description: 'Outstanding shipping carrier invoices', isReconciliationRequired: true },
  { accountNumber: '202000', accountName: 'Sales & Use Tax Payable - United States', accountCategory: 'LIABILITY', normalBalance: 'CREDIT', description: 'Collected sales taxes due to state tax authorities', isReconciliationRequired: true },
  { accountNumber: '202010', accountName: 'Value Added Tax (VAT) Payable - European Union', accountCategory: 'LIABILITY', normalBalance: 'CREDIT', description: 'Collected VAT due to EU tax administrations', isReconciliationRequired: true },
  { accountNumber: '203000', accountName: 'Unearned Revenue - Customer Gift Cards', accountCategory: 'LIABILITY', normalBalance: 'CREDIT', description: 'Outstanding customer store credits and gift cards', isReconciliationRequired: true },
  { accountNumber: '204000', accountName: 'Accrued Customer Refunds & Returns', accountCategory: 'LIABILITY', normalBalance: 'CREDIT', description: 'Estimated pending RMA refund payouts', isReconciliationRequired: true },
  { accountNumber: '205000', accountName: 'Marketplace Seller Escrow Payable', accountCategory: 'LIABILITY', normalBalance: 'CREDIT', description: 'Held funds pending seller delivery confirmation', isReconciliationRequired: true },
  { accountNumber: '301000', accountName: 'Common Stock Capital', accountCategory: 'EQUITY', normalBalance: 'CREDIT', description: 'Par value of issued common equity shares', isReconciliationRequired: false },
  { accountNumber: '302000', accountName: 'Additional Paid-In Capital (APIC)', accountCategory: 'EQUITY', normalBalance: 'CREDIT', description: 'Capital contributions in excess of par value', isReconciliationRequired: false },
  { accountNumber: '303000', accountName: 'Retained Earnings - Cumulative', accountCategory: 'EQUITY', normalBalance: 'CREDIT', description: 'Cumulative net income retained in the business', isReconciliationRequired: false },
  { accountNumber: '401000', accountName: 'Gross Sales Revenue - Enterprise Hardware', accountCategory: 'REVENUE', normalBalance: 'CREDIT', description: 'Gross sales value from servers, laptops, and networking gear', isReconciliationRequired: false },
  { accountNumber: '402000', accountName: 'Shipping & Handling Fee Income', accountCategory: 'REVENUE', normalBalance: 'CREDIT', description: 'Customer-paid delivery and freight fees', isReconciliationRequired: false },
  { accountNumber: '403000', accountName: 'Marketplace Platform Commission Fee Income', accountCategory: 'REVENUE', normalBalance: 'CREDIT', description: 'Transaction take-rate fees charged to 3rd party sellers', isReconciliationRequired: false },
  { accountNumber: '409000', accountName: 'Customer Sales Discounts & Promo Coupons (Contra)', accountCategory: 'REVENUE', normalBalance: 'DEBIT', description: 'Coupons and promotional discounts deducted from sales', isReconciliationRequired: false },
  { accountNumber: '409010', accountName: 'Customer Returns & Allowances (Contra)', accountCategory: 'REVENUE', normalBalance: 'DEBIT', description: 'Refunds and price concessions granted on returned goods', isReconciliationRequired: false },
  { accountNumber: '501000', accountName: 'Cost of Goods Sold - Hardware Products', accountCategory: 'COST_OF_GOODS', normalBalance: 'DEBIT', description: 'Cost of inventory sold during the accounting period', isReconciliationRequired: false },
  { accountNumber: '502000', accountName: 'Carrier Outbound Freight Shipping Expense', accountCategory: 'COST_OF_GOODS', normalBalance: 'DEBIT', description: 'Direct courier shipping expenses paid to FedEx, UPS, DHL', isReconciliationRequired: false },
  { accountNumber: '503000', accountName: 'Warehouse Packaging & Supplies Expense', accountCategory: 'COST_OF_GOODS', normalBalance: 'DEBIT', description: 'Boxes, dunnage, thermal labels, and pallets', isReconciliationRequired: false },
  { accountNumber: '504000', accountName: 'Inventory Scrap & Write-Down Expense', accountCategory: 'COST_OF_GOODS', normalBalance: 'DEBIT', description: 'Damaged goods discarded during RMA inspection', isReconciliationRequired: false },
  { accountNumber: '601000', accountName: 'Payment Gateway Merchant Processing Fees', accountCategory: 'OPERATING_EXPENSE', normalBalance: 'DEBIT', description: 'Interchange fees, Stripe 2.9% + 30c, and bank fees', isReconciliationRequired: false },
  { accountNumber: '602000', accountName: 'Cloud Computing & Data Infrastructure', accountCategory: 'OPERATING_EXPENSE', normalBalance: 'DEBIT', description: 'AWS, GCP, Kubernetes hosting, and CDN costs', isReconciliationRequired: false },
  { accountNumber: '603000', accountName: 'Customer Support & Chargeback Loss Expense', accountCategory: 'OPERATING_EXPENSE', normalBalance: 'DEBIT', description: 'Dispute fees and unrecoverable fraudulent chargebacks', isReconciliationRequired: false },
];

export class GeneralLedgerChartOfAccounts {
  public static getAccount(accountNumber: string): GlAccountRecord | undefined {
    return MASTER_CHART_OF_ACCOUNTS.find(a => a.accountNumber === accountNumber);
  }

  public static getAccountsByCategory(category: GlAccountRecord['accountCategory']): GlAccountRecord[] {
    return MASTER_CHART_OF_ACCOUNTS.filter(a => a.accountCategory === category);
  }
}
