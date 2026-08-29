export interface AccountDefinition {
  accountNumber: string;
  name: string;
  category: 'ASSET' | 'LIABILITY' | 'EQUITY' | 'REVENUE' | 'EXPENSE';
  normalBalance: 'DEBIT' | 'CREDIT';
  description: string;
}

export const CHART_OF_ACCOUNTS: Record<string, AccountDefinition> = {
  // Assets (1000 - 1999)
  '1010': { accountNumber: '1010', name: 'Operating Cash & Bank Account', category: 'ASSET', normalBalance: 'DEBIT', description: 'Primary corporate checking balance for settlement' },
  '1020': { accountNumber: '1020', name: 'Stripe Processor Clearing Account', category: 'ASSET', normalBalance: 'DEBIT', description: 'Pending in-transit funds from Stripe gateway' },
  '1030': { accountNumber: '1030', name: 'PayPal Processor Clearing Account', category: 'ASSET', normalBalance: 'DEBIT', description: 'Pending in-transit funds from PayPal gateway' },
  '1040': { accountNumber: '1040', name: 'Accounts Receivable', category: 'ASSET', normalBalance: 'DEBIT', description: 'Invoiced corporate credit terms customer balances' },
  '1050': { accountNumber: '1050', name: 'Inventory Asset - On-Hand Stock', category: 'ASSET', normalBalance: 'DEBIT', description: 'Valuation of warehouse merchandise inventory' },
  '1060': { accountNumber: '1060', name: 'Prepaid Expenses & Retainers', category: 'ASSET', normalBalance: 'DEBIT', description: 'Advance payments for hosting, carriers, software' },

  // Liabilities (2000 - 2999)
  '2010': { accountNumber: '2010', name: 'Accounts Payable', category: 'ASSET', normalBalance: 'CREDIT', description: 'Supplier and carrier unpaid vendor bills' },
  '2020': { accountNumber: '2020', name: 'Sales Tax Payable - State Jurisdictions', category: 'LIABILITY', normalBalance: 'CREDIT', description: 'Collected sales tax awaiting monthly/quarterly remittance' },
  '2030': { accountNumber: '2030', name: 'Unearned Revenue / Gift Card Liability', category: 'LIABILITY', normalBalance: 'CREDIT', description: 'Pre-paid store credit and outstanding gift certificates' },
  '2040': { accountNumber: '2040', name: 'Customer Refund Reserve Liability', category: 'LIABILITY', normalBalance: 'CREDIT', description: 'Provision for returns, dispute chargebacks, and warranties' },

  // Equity (3000 - 3999)
  '3010': { accountNumber: '3010', name: 'Common Stock Capital', category: 'EQUITY', normalBalance: 'CREDIT', description: 'Paid-in equity capital' },
  '3020': { accountNumber: '3020', name: 'Retained Earnings', category: 'EQUITY', normalBalance: 'CREDIT', description: 'Cumulative historical net operating profit' },

  // Revenues (4000 - 4999)
  '4010': { accountNumber: '4010', name: 'Product Sales Gross Revenue', category: 'REVENUE', normalBalance: 'CREDIT', description: 'Primary gross merchandise volume (GMV) revenue' },
  '4020': { accountNumber: '4020', name: 'Shipping & Delivery Fee Income', category: 'REVENUE', normalBalance: 'CREDIT', description: 'Customer payments for freight and expedited courier' },
  '4030': { accountNumber: '4030', name: 'Subscription & Membership Fees', category: 'REVENUE', normalBalance: 'CREDIT', description: 'Recurring premium VIP membership program fees' },
  '4090': { accountNumber: '4090', name: 'Sales Discounts & Coupon Allowances', category: 'REVENUE', normalBalance: 'DEBIT', description: 'Contra-revenue account tracking promotional discounts' },

  // Cost of Goods & Operating Expenses (5000 - 6999)
  '5010': { accountNumber: '5010', name: 'Cost of Goods Sold (COGS)', category: 'EXPENSE', normalBalance: 'DEBIT', description: 'Direct acquisition/manufacturing cost of sold inventory' },
  '5020': { accountNumber: '5020', name: 'Carrier Freight & Packaging Cost', category: 'EXPENSE', normalBalance: 'DEBIT', description: 'Direct courier bills from FedEx, UPS, DHL' },
  '5030': { accountNumber: '5030', name: 'Payment Gateway Processing Fees', category: 'EXPENSE', normalBalance: 'DEBIT', description: 'Merchant interchange, 2.9% + 30c processor costs' },
  '6010': { accountNumber: '6010', name: 'Cloud Infrastructure & Hosting Expenses', category: 'EXPENSE', normalBalance: 'DEBIT', description: 'Kubernetes, AWS, database, Redis server expenditures' }
};
