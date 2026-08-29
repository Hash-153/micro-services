import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def build_payment_advanced():
    print("Generating Payment Advanced...")

    write_file("services/payment-service/src/domain/luhn-validator.ts", """export type CardBrand = 'VISA' | 'MASTERCARD' | 'AMEX' | 'DISCOVER' | 'JCB' | 'DINERS_CLUB' | 'UNKNOWN';

export interface CardValidationResult {
  isValidLuhn: boolean;
  brand: CardBrand;
  isSupported: boolean;
  lastFourDigits: string;
  bin: string;
}

export class LuhnCardValidator {
  public static validate(cardNumber: string): CardValidationResult {
    const cleanNumber = cardNumber.replace(/[\\s-]/g, '');
    const isValidLuhn = this.checkLuhn(cleanNumber);
    const brand = this.detectBrand(cleanNumber);
    const lastFourDigits = cleanNumber.slice(-4);
    const bin = cleanNumber.slice(0, 6);

    const isSupported = ['VISA', 'MASTERCARD', 'AMEX', 'DISCOVER'].includes(brand);

    return {
      isValidLuhn,
      brand,
      isSupported,
      lastFourDigits,
      bin
    };
  }

  private static checkLuhn(numberStr: string): boolean {
    if (!/^[0-9]{13,19}$/.test(numberStr)) {
      return false;
    }

    let sum = 0;
    let shouldDouble = false;

    for (let i = numberStr.length - 1; i >= 0; i--) {
      let digit = parseInt(numberStr.charAt(i), 10);

      if (shouldDouble) {
        digit *= 2;
        if (digit > 9) {
          digit -= 9;
        }
      }

      sum += digit;
      shouldDouble = !shouldDouble;
    }

    return sum % 10 === 0;
  }

  private static detectBrand(numberStr: string): CardBrand {
    if (/^4[0-9]{12}(?:[0-9]{3})?$/.test(numberStr)) {
      return 'VISA';
    }
    if (/^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$/.test(numberStr)) {
      return 'MASTERCARD';
    }
    if (/^3[47][0-9]{13}$/.test(numberStr)) {
      return 'AMEX';
    }
    if (/^6(?:011|5[0-9]{2})[0-9]{12}$/.test(numberStr)) {
      return 'DISCOVER';
    }
    if (/^(?:2131|1800|35\\d{3})\\d{11}$/.test(numberStr)) {
      return 'JCB';
    }
    if (/^3(?:0[0-5]|[68][0-9])[0-9]{11}$/.test(numberStr)) {
      return 'DINERS_CLUB';
    }
    return 'UNKNOWN';
  }
}
""")

    write_file("services/payment-service/src/domain/payout-calculator.ts", """export interface MarketplacePayoutSplit {
  orderTotalCents: number;
  platformFeePercent: number;
  platformFeeCents: number;
  gatewayFeeCents: number;
  merchantNetPayoutCents: number;
  reserveHoldbackCents: number;
  reserveHoldbackDays: number;
}

export class PayoutCalculator {
  public static calculateSplit(
    orderTotalCents: number,
    platformFeePercent: number = 8.5,
    reserveHoldbackPercent: number = 5.0,
    reserveHoldbackDays: number = 14
  ): MarketplacePayoutSplit {
    const platformFeeCents = Math.round((orderTotalCents * platformFeePercent) / 100);
    const gatewayFeeCents = Math.round(orderTotalCents * 0.029 + 30); // 2.9% + 30c
    const reserveHoldbackCents = Math.round((orderTotalCents * reserveHoldbackPercent) / 100);

    const merchantNetPayoutCents = Math.max(
      0,
      orderTotalCents - platformFeeCents - gatewayFeeCents - reserveHoldbackCents
    );

    return {
      orderTotalCents,
      platformFeePercent,
      platformFeeCents,
      gatewayFeeCents,
      merchantNetPayoutCents,
      reserveHoldbackCents,
      reserveHoldbackDays
    };
  }
}
""")

    write_file("services/payment-service/src/domain/sub-ledger-hierarchy.ts", """export interface SubLedgerAccount {
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
""")

    print("Payment advanced complete.")

if __name__ == "__main__":
    build_payment_advanced()
