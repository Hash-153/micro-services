import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_bulk_engine_modules():
    print("Generating comprehensive Bulk Engine Modules...")

    # 1. Payment Merchant Chargeback Reason Code Classifier
    write_file("services/payment-service/src/domain/chargeback-reason-codes.ts", """export interface ChargebackReasonDefinition {
  cardScheme: 'VISA' | 'MASTERCARD' | 'AMEX' | 'DISCOVER';
  reasonCode: string;
  category: 'FRAUD' | 'AUTHORIZATION' | 'PROCESSING_ERROR' | 'CUSTOMER_DISPUTE';
  description: string;
  compellingEvidenceRequirements: string[];
}

export const CHARGEBACK_REASON_CATALOG: ChargebackReasonDefinition[] = [
  // Visa Codes
  {
    cardScheme: 'VISA',
    reasonCode: '10.4',
    category: 'FRAUD',
    description: 'Other Fraud - Card-Absent Environment',
    compellingEvidenceRequirements: ['IP address match', 'AVS full match', 'Proof of delivery signed by recipient', 'Device fingerprint logs']
  },
  {
    cardScheme: 'VISA',
    reasonCode: '13.1',
    category: 'CUSTOMER_DISPUTE',
    description: 'Merchandise / Services Not Received',
    compellingEvidenceRequirements: ['Carrier delivery confirmation', 'GPS coordinates at delivery scan', 'Signature image']
  },
  {
    cardScheme: 'VISA',
    reasonCode: '13.3',
    category: 'CUSTOMER_DISPUTE',
    description: 'Not as Described or Defective Merchandise',
    compellingEvidenceRequirements: ['Detailed product catalog specification', 'Email communication thread', 'Return policy acceptance timestamp']
  },
  
  // Mastercard Codes
  {
    cardScheme: 'MASTERCARD',
    reasonCode: '4837',
    category: 'FRAUD',
    description: 'No Cardholder Authorization',
    compellingEvidenceRequirements: ['EMV 3D-Secure CAVV / ECI token', 'Billing address verification (AVS)', 'CVC2 verification match']
  },
  {
    cardScheme: 'MASTERCARD',
    reasonCode: '4853',
    category: 'CUSTOMER_DISPUTE',
    description: 'Recurring Transaction Cancelled or Defective Goods',
    compellingEvidenceRequirements: ['Terms of service clickwrap log', 'Cancellation policy link', 'Active customer login history']
  }
];

export class ChargebackClassifier {
  public static findReason(cardScheme: string, reasonCode: string): ChargebackReasonDefinition | undefined {
    return CHARGEBACK_REASON_CATALOG.find(
      r => r.cardScheme.toUpperCase() === cardScheme.toUpperCase() && r.reasonCode === reasonCode
    );
  }
}
""")

    # 2. Fulfillment Dimension Volume Divisor Matrix (IATA vs Domestic)
    write_file("services/fulfillment-service/src/domain/dimensional-weight-matrix.ts", """import { Dimensions3D } from '@novacommerce/core-types';

export interface DimensionalWeightRule {
  carrier: string;
  serviceType: 'DOMESTIC' | 'INTERNATIONAL';
  dimensionalDivisorCm: number; // e.g. 5000 for IATA (cm3/kg) or 139 for US inches (in3/lb)
  minimumBillableWeightGrams: number;
}

export const DIMENSIONAL_WEIGHT_RULES: DimensionalWeightRule[] = [
  { carrier: 'FEDEX', serviceType: 'DOMESTIC', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 500 },
  { carrier: 'FEDEX', serviceType: 'INTERNATIONAL', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 1000 },
  { carrier: 'UPS', serviceType: 'DOMESTIC', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 500 },
  { carrier: 'UPS', serviceType: 'INTERNATIONAL', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 1000 },
  { carrier: 'DHL', serviceType: 'INTERNATIONAL', dimensionalDivisorCm: 5000, minimumBillableWeightGrams: 500 }
];

export class DimensionalWeightCalculator {
  public static calculateBillableWeightGrams(
    actualWeightGrams: number,
    dimensionsMm: Dimensions3D,
    carrier: string = 'FEDEX',
    serviceType: 'DOMESTIC' | 'INTERNATIONAL' = 'DOMESTIC'
  ): { billableWeightGrams: number; volumetricWeightGrams: number; isVolumetricApplied: boolean } {
    const rule = DIMENSIONAL_WEIGHT_RULES.find(r => r.carrier === carrier && r.serviceType === serviceType) || DIMENSIONAL_WEIGHT_RULES[0];

    // Volume in cubic centimeters
    const volumeCm3 = (dimensionsMm.length / 10) * (dimensionsMm.width / 10) * (dimensionsMm.height / 10);
    const volumetricKg = volumeCm3 / rule.dimensionalDivisorCm;
    const volumetricGrams = Math.round(volumetricKg * 1000);

    const billable = Math.max(actualWeightGrams, volumetricGrams, rule.minimumBillableWeightGrams);

    return {
      billableWeightGrams: billable,
      volumetricWeightGrams: volumetricGrams,
      isVolumetricApplied: volumetricGrams > actualWeightGrams
    };
  }
}
""")

    print("Bulk engine modules generated.")

if __name__ == "__main__":
    generate_bulk_engine_modules()
