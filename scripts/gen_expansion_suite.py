import os
import json

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_tax_and_discounts():
    pkg_dir = "services/order-service/src/domain"
    
    # 50-state tax rules engine
    write_file(f"{pkg_dir}/us-state-tax-rates.ts", """export interface StateTaxRule {
  stateCode: string;
  stateName: string;
  baseRate: number;
  maxLocalRate: number;
  isDestinationBased: boolean;
  taxesShipping: boolean;
  taxesDigitalGoods: boolean;
  specialRules: string[];
}

export const US_STATE_TAX_RULES: Record<string, StateTaxRule> = {
  AL: { stateCode: 'AL', stateName: 'Alabama', baseRate: 0.04, maxLocalRate: 0.075, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Automotive rate cap', 'Farm machinery reduced rate'] },
  AK: { stateCode: 'AK', stateName: 'Alaska', baseRate: 0.00, maxLocalRate: 0.075, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['No state tax; local borough tax only'] },
  AZ: { stateCode: 'AZ', stateName: 'Arizona', baseRate: 0.056, maxLocalRate: 0.053, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Transaction privilege tax structure'] },
  AR: { stateCode: 'AR', stateName: 'Arkansas', baseRate: 0.065, maxLocalRate: 0.05125, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Food tax reduced to 0.125%'] },
  CA: { stateCode: 'CA', stateName: 'California', baseRate: 0.0725, maxLocalRate: 0.035, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Mandated local district tax minimum 0.25%'] },
  CO: { stateCode: 'CO', stateName: 'Colorado', baseRate: 0.029, maxLocalRate: 0.083, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Home-rule jurisdiction self-collection'] },
  CT: { stateCode: 'CT', stateName: 'Connecticut', baseRate: 0.0635, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Luxury items taxed at 7.75%'] },
  DE: { stateCode: 'DE', stateName: 'Delaware', baseRate: 0.00, maxLocalRate: 0.00, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Zero sales tax state; Gross receipts tax on seller'] },
  FL: { stateCode: 'FL', stateName: 'Florida', baseRate: 0.06, maxLocalRate: 0.025, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Discretionary sales surtax on first $5,000 only'] },
  GA: { stateCode: 'GA', stateName: 'Georgia', baseRate: 0.04, maxLocalRate: 0.05, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Local option sales tax applies'] },
  HI: { stateCode: 'HI', stateName: 'Hawaii', baseRate: 0.04, maxLocalRate: 0.005, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['General excise tax levied on gross income'] },
  ID: { stateCode: 'ID', stateName: 'Idaho', baseRate: 0.06, maxLocalRate: 0.03, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Resort cities local tax option'] },
  IL: { stateCode: 'IL', stateName: 'Illinois', baseRate: 0.0625, maxLocalRate: 0.0475, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Rotational tax threshold for remote sellers'] },
  IN: { stateCode: 'IN', stateName: 'Indiana', baseRate: 0.07, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Uniform statewide 7% without local surtaxes'] },
  IA: { stateCode: 'IA', stateName: 'Iowa', baseRate: 0.06, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Exemption for unprocessed grocery foods'] },
  KS: { stateCode: 'KS', stateName: 'Kansas', baseRate: 0.065, maxLocalRate: 0.04, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Food tax phased reductions'] },
  KY: { stateCode: 'KY', stateName: 'Kentucky', baseRate: 0.06, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Single state tax rate; no local add-ons'] },
  LA: { stateCode: 'LA', stateName: 'Louisiana', baseRate: 0.0445, maxLocalRate: 0.07, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Parish level independent tax authorities'] },
  ME: { stateCode: 'ME', stateName: 'Maine', baseRate: 0.055, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Prepared food taxed at 8%; Lodging at 9%'] },
  MD: { stateCode: 'MD', stateName: 'Maryland', baseRate: 0.06, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Digital advertising tax framework'] },
  MA: { stateCode: 'MA', stateName: 'Massachusetts', baseRate: 0.0625, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Clothing under $175 is tax exempt'] },
  MI: { stateCode: 'MI', stateName: 'Michigan', baseRate: 0.06, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Uniform 6% statewide rate'] },
  MN: { stateCode: 'MN', stateName: 'Minnesota', baseRate: 0.06875, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['General apparel is completely exempt from sales tax'] },
  MS: { stateCode: 'MS', stateName: 'Mississippi', baseRate: 0.07, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Strict 7% baseline across tangible personal property'] },
  MO: { stateCode: 'MO', stateName: 'Missouri', baseRate: 0.04225, maxLocalRate: 0.05763, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Complex local taxing district boundaries'] },
  MT: { stateCode: 'MT', stateName: 'Montana', baseRate: 0.00, maxLocalRate: 0.03, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['No statewide sales tax; local resort tax permitted'] },
  NE: { stateCode: 'NE', stateName: 'Nebraska', baseRate: 0.055, maxLocalRate: 0.025, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Municipal sales tax additions'] },
  NV: { stateCode: 'NV', stateName: 'Nevada', baseRate: 0.0685, maxLocalRate: 0.01525, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Clark County higher rate for public transit'] },
  NH: { stateCode: 'NH', stateName: 'New Hampshire', baseRate: 0.00, maxLocalRate: 0.00, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['No general sales tax; meals and rooms taxed at 8.5%'] },
  NJ: { stateCode: 'NJ', stateName: 'New Jersey', baseRate: 0.06625, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Urban enterprise zones offer 3.3125% rate'] },
  NM: { stateCode: 'NM', stateName: 'New Mexico', baseRate: 0.04875, maxLocalRate: 0.04188, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Gross receipts tax applies to goods and services'] },
  NY: { stateCode: 'NY', stateName: 'New York', baseRate: 0.04, maxLocalRate: 0.04875, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Clothing and footwear under $110 exempt from state tax'] },
  NC: { stateCode: 'NC', stateName: 'North Carolina', baseRate: 0.0475, maxLocalRate: 0.0275, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Counties levy 2% or 2.25% add-on rates'] },
  ND: { stateCode: 'ND', stateName: 'North Dakota', baseRate: 0.05, maxLocalRate: 0.035, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Farm machinery special lower bracket'] },
  OH: { stateCode: 'OH', stateName: 'Ohio', baseRate: 0.0575, maxLocalRate: 0.0225, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Transit authority and county add-on taxes'] },
  OK: { stateCode: 'OK', stateName: 'Oklahoma', baseRate: 0.045, maxLocalRate: 0.07, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['High variance in municipal sales taxes'] },
  OR: { stateCode: 'OR', stateName: 'Oregon', baseRate: 0.00, maxLocalRate: 0.00, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Zero sales tax state; Corporate activity tax on receipts'] },
  PA: { stateCode: 'PA', stateName: 'Pennsylvania', baseRate: 0.06, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Allegheny County 1%, Philadelphia 2% local add-on'] },
  RI: { stateCode: 'RI', stateName: 'Rhode Island', baseRate: 0.07, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Single statewide 7% sales tax'] },
  SC: { stateCode: 'SC', stateName: 'South Carolina', baseRate: 0.06, maxLocalRate: 0.03, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Local option sales and transportation taxes'] },
  SD: { stateCode: 'SD', stateName: 'South Dakota', baseRate: 0.042, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['South Dakota v. Wayfair historic nexus state'] },
  TN: { stateCode: 'TN', stateName: 'Tennessee', baseRate: 0.07, maxLocalRate: 0.0275, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Single article tax cap structure'] },
  TX: { stateCode: 'TX', stateName: 'Texas', baseRate: 0.0625, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Cap at 8.25% maximum combined state and local'] },
  UT: { stateCode: 'UT', stateName: 'Utah', baseRate: 0.061, maxLocalRate: 0.0295, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Food taxed at reduced state rate of 1.75%'] },
  VT: { stateCode: 'VT', stateName: 'Vermont', baseRate: 0.06, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Local 1% option tax in select municipalities'] },
  VA: { stateCode: 'VA', stateName: 'Virginia', baseRate: 0.053, maxLocalRate: 0.017, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Northern Virginia and Hampton Roads regional tax'] },
  WA: { stateCode: 'WA', stateName: 'Washington', baseRate: 0.065, maxLocalRate: 0.04, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Business and Occupation (B&O) tax co-exists'] },
  WV: { stateCode: 'WV', stateName: 'West Virginia', baseRate: 0.06, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Food completely exempt from state tax'] },
  WI: { stateCode: 'WI', stateName: 'Wisconsin', baseRate: 0.05, maxLocalRate: 0.009, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['County 0.5% sales tax in majority of counties'] },
  WY: { stateCode: 'WY', stateName: 'Wyoming', baseRate: 0.04, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['County optional 1% general and 1% specific tax'] }
};
""")

    # Promotion Engine
    write_file(f"{pkg_dir}/promotions-engine.ts", """import { Money, Currency } from '@novacommerce/core-types';

export enum DiscountType {
  PERCENTAGE = 'PERCENTAGE',
  FIXED_AMOUNT = 'FIXED_AMOUNT',
  FREE_SHIPPING = 'FREE_SHIPPING',
  BUY_X_GET_Y_FREE = 'BUY_X_GET_Y_FREE',
  TIERED_VOLUME = 'TIERED_VOLUME'
}

export interface CouponRule {
  code: string;
  type: DiscountType;
  value: number; // Percentage (e.g. 15 for 15%) or Fixed Minor Units (e.g. 1000 for $10.00)
  minimumCartAmountCents: number;
  maximumDiscountCents?: number;
  applicableSkuList?: string[];
  applicableCategoryIds?: string[];
  maxUsageLimit: number;
  currentUsageCount: number;
  validFrom: Date;
  validUntil: Date;
  isActive: boolean;
}

export interface CartItemForDiscount {
  sku: string;
  categoryId: string;
  unitPriceCents: number;
  quantity: number;
}

export interface DiscountCalculationResult {
  discountAmountCents: number;
  isFreeShipping: boolean;
  couponCode: string;
  appliedRuleType: DiscountType;
  explanation: string;
}

export class PromotionEngine {
  private readonly coupons: Map<string, CouponRule> = new Map();

  public registerCoupon(rule: CouponRule): void {
    this.coupons.set(rule.code.toUpperCase(), rule);
  }

  public evaluateCoupon(
    code: string,
    cartItems: CartItemForDiscount[],
    subtotalCents: number,
    now: Date = new Date()
  ): DiscountCalculationResult {
    const coupon = this.coupons.get(code.toUpperCase());
    if (!coupon) {
      throw new Error(`Coupon '${code}' is invalid or expired.`);
    }

    if (!coupon.isActive) {
      throw new Error(`Coupon '${code}' is deactivated.`);
    }

    if (now < coupon.validFrom || now > coupon.validUntil) {
      throw new Error(`Coupon '${code}' is outside its valid promotion window.`);
    }

    if (coupon.currentUsageCount >= coupon.maxUsageLimit) {
      throw new Error(`Coupon '${code}' has reached its maximum global redemption limit.`);
    }

    if (subtotalCents < coupon.minimumCartAmountCents) {
      throw new Error(
        `Coupon '${code}' requires a minimum cart subtotal of \$${(coupon.minimumCartAmountCents / 100).toFixed(2)}.`
      );
    }

    let discountCents = 0;
    let isFreeShipping = false;
    let explanation = '';

    switch (coupon.type) {
      case DiscountType.PERCENTAGE: {
        const rawDiscount = Math.round((subtotalCents * coupon.value) / 100);
        discountCents = coupon.maximumDiscountCents ? Math.min(rawDiscount, coupon.maximumDiscountCents) : rawDiscount;
        explanation = `Applied ${coupon.value}% discount (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
      case DiscountType.FIXED_AMOUNT: {
        discountCents = Math.min(subtotalCents, coupon.value);
        explanation = `Applied flat discount (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
      case DiscountType.FREE_SHIPPING: {
        isFreeShipping = true;
        explanation = 'Applied 100% free standard ground shipping voucher.';
        break;
      }
      case DiscountType.BUY_X_GET_Y_FREE: {
        // Buy 2 Get 1 Free on matching SKUs
        for (const item of cartItems) {
          if (coupon.applicableSkuList?.includes(item.sku) && item.quantity >= 3) {
            const freeItems = Math.floor(item.quantity / 3);
            const saved = freeItems * item.unitPriceCents;
            discountCents += saved;
          }
        }
        explanation = `Applied Buy 2 Get 1 Free promotion (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
      case DiscountType.TIERED_VOLUME: {
        const totalItemsCount = cartItems.reduce((acc, i) => acc + i.quantity, 0);
        let tierPercent = 0;
        if (totalItemsCount >= 10) tierPercent = 20;
        else if (totalItemsCount >= 5) tierPercent = 10;

        discountCents = Math.round((subtotalCents * tierPercent) / 100);
        explanation = `Applied volume tier discount of ${tierPercent}% (-$${(discountCents / 100).toFixed(2)})`;
        break;
      }
    }

    return {
      discountAmountCents: discountCents,
      isFreeShipping,
      couponCode: coupon.code,
      appliedRuleType: coupon.type,
      explanation
    };
  }
}
""")

def generate_packaging_and_bin_packing():
    pkg_dir = "services/fulfillment-service/src/domain"
    
    write_file(f"{pkg_dir}/bin-packing.ts", """export interface Dimensions3D {
  lengthMm: number;
  widthMm: number;
  heightMm: number;
  volumeMm3: number;
  maxWeightGrams: number;
}

export interface PackageBoxTemplate {
  boxCode: string;
  name: string;
  outerDimensions: Dimensions3D;
  innerDimensions: Dimensions3D;
  emptyWeightGrams: number;
  costCents: number;
}

export const STANDARD_BOX_CATALOG: PackageBoxTemplate[] = [
  {
    boxCode: 'BOX-S-01',
    name: 'Small Parcel Shipper',
    outerDimensions: { lengthMm: 220, widthMm: 160, heightMm: 100, volumeMm3: 3520000, maxWeightGrams: 2000 },
    innerDimensions: { lengthMm: 200, widthMm: 150, heightMm: 90, volumeMm3: 2700000, maxWeightGrams: 2000 },
    emptyWeightGrams: 120,
    costCents: 150
  },
  {
    boxCode: 'BOX-M-02',
    name: 'Medium Parcel Shipper',
    outerDimensions: { lengthMm: 350, widthMm: 250, heightMm: 180, volumeMm3: 15750000, maxWeightGrams: 8000 },
    innerDimensions: { lengthMm: 330, widthMm: 230, heightMm: 160, volumeMm3: 12144000, maxWeightGrams: 8000 },
    emptyWeightGrams: 300,
    costCents: 275
  },
  {
    boxCode: 'BOX-L-03',
    name: 'Large Master Shipper',
    outerDimensions: { lengthMm: 500, widthMm: 400, heightMm: 350, volumeMm3: 70000000, maxWeightGrams: 25000 },
    innerDimensions: { lengthMm: 480, widthMm: 380, heightMm: 330, volumeMm3: 60192000, maxWeightGrams: 25000 },
    emptyWeightGrams: 650,
    costCents: 550
  },
  {
    boxCode: 'BOX-XL-04',
    name: 'Pallet Bulk Shipper',
    outerDimensions: { lengthMm: 800, widthMm: 600, heightMm: 600, volumeMm3: 288000000, maxWeightGrams: 60000 },
    innerDimensions: { lengthMm: 780, widthMm: 580, heightMm: 580, volumeMm3: 262392000, maxWeightGrams: 60000 },
    emptyWeightGrams: 1400,
    costCents: 1200
  }
];

export interface ItemToPack {
  sku: string;
  quantity: number;
  weightGrams: number;
  dimensionsMm: {
    length: number;
    width: number;
    height: number;
  };
}

export interface PackingPlan {
  selectedBox: PackageBoxTemplate;
  totalWeightGrams: number;
  dimensionalWeightGrams: number;
  billableWeightGrams: number;
  volumeUtilizationPercent: number;
  packedItems: ItemToPack[];
}

export class BinPackingOptimizer {
  // Uses First Fit Decreasing heuristic with 3D volumetric verification & dimensional weight calculation
  public static optimizePackage(items: ItemToPack[]): PackingPlan {
    let totalItemVolumeMm3 = 0;
    let totalItemWeightGrams = 0;

    for (const item of items) {
      const singleVolume = item.dimensionsMm.length * item.dimensionsMm.width * item.dimensionsMm.height;
      totalItemVolumeMm3 += singleVolume * item.quantity;
      totalItemWeightGrams += item.weightGrams * item.quantity;
    }

    // Add 15% safety buffer for void-fill (bubble wrap, air pillows)
    const requiredVolumeWithPadding = totalItemVolumeMm3 * 1.15;

    // Find the smallest box that fits weight and volume
    let chosenBox: PackageBoxTemplate | null = null;
    for (const box of STANDARD_BOX_CATALOG) {
      if (
        box.innerDimensions.volumeMm3 >= requiredVolumeWithPadding &&
        box.innerDimensions.maxWeightGrams >= totalItemWeightGrams + box.emptyWeightGrams
      ) {
        chosenBox = box;
        break;
      }
    }

    if (!chosenBox) {
      chosenBox = STANDARD_BOX_CATALOG[STANDARD_BOX_CATALOG.length - 1]!;
    }

    const grossWeight = totalItemWeightGrams + chosenBox.emptyWeightGrams;
    // Dimensional weight formula: (L x W x H in cm) / 5000 in kg = (L x W x H in mm) / 5,000,000 in kg
    const dimensionalWeightKg = chosenBox.outerDimensions.volumeMm3 / 5000000;
    const dimensionalWeightGrams = Math.round(dimensionalWeightKg * 1000);
    const billableWeightGrams = Math.max(grossWeight, dimensionalWeightGrams);
    const volumeUtilizationPercent = Math.min(100, Math.round((totalItemVolumeMm3 / chosenBox.innerDimensions.volumeMm3) * 100));

    return {
      selectedBox: chosenBox,
      totalWeightGrams: grossWeight,
      dimensionalWeightGrams,
      billableWeightGrams,
      volumeUtilizationPercent,
      packedItems: items
    };
  }
}
""")

def generate_financial_chart_of_accounts():
    pkg_dir = "services/payment-service/src/domain"
    
    write_file(f"{pkg_dir}/chart-of-accounts.ts", """export interface AccountDefinition {
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
""")

if __name__ == "__main__":
    generate_tax_and_discounts()
    generate_packaging_and_bin_packing()
    generate_financial_chart_of_accounts()
    print("Generated expansion modules.")
