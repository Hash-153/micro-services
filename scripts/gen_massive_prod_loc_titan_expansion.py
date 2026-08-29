import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_titan_expansion_modules():
    print("Generating comprehensive Titan Expansion Modules...")

    # 1. Payment ISO 8583 Authorization Response Code Mapper
    write_file("services/payment-service/src/domain/iso8583-response-mapper.ts", """export interface IsoResponseCodeDefinition {
  responseCode: string;
  category: 'APPROVED' | 'DECLINED' | 'CALL_ISSUER' | 'FRAUD_SUSPECT' | 'SYSTEM_ERROR';
  description: string;
  isRetryable: boolean;
  actionRequired: string;
}

export const ISO8583_RESPONSE_CODES: Record<string, IsoResponseCodeDefinition> = {
  '00': { responseCode: '00', category: 'APPROVED', description: 'Approved and completed successfully', isRetryable: false, actionRequired: 'Proceed with order capture' },
  '01': { responseCode: '01', category: 'CALL_ISSUER', description: 'Refer to card issuer for voice authorization', isRetryable: false, actionRequired: 'Customer must contact their issuing bank' },
  '04': { responseCode: '04', category: 'FRAUD_SUSPECT', description: 'Pick up card (fraud suspect / stolen card)', isRetryable: false, actionRequired: 'Block account and cancel transaction immediately' },
  '05': { responseCode: '05', category: 'DECLINED', description: 'Do not honor (general decline by bank risk engine)', isRetryable: false, actionRequired: 'Request an alternative payment method' },
  '12': { responseCode: '12', category: 'SYSTEM_ERROR', description: 'Invalid transaction structure or missing field', isRetryable: false, actionRequired: 'Inspect payload validation rules' },
  '14': { responseCode: '14', category: 'DECLINED', description: 'Invalid card number (no such PAN on file)', isRetryable: false, actionRequired: 'Prompt user to re-enter card details' },
  '51': { responseCode: '51', category: 'DECLINED', description: 'Insufficient funds / credit limit exceeded', isRetryable: true, actionRequired: 'Prompt user to use alternative card' },
  '54': { responseCode: '54', category: 'DECLINED', description: 'Expired card', isRetryable: false, actionRequired: 'Prompt user to update expiration date' },
  '57': { responseCode: '57', category: 'DECLINED', description: 'Transaction not permitted to cardholder (e.g. cross-border restriction)', isRetryable: false, actionRequired: 'Customer must enable international transactions' },
  '65': { responseCode: '65', category: 'DECLINED', description: 'Activity count limit exceeded (daily velocity)', isRetryable: true, actionRequired: 'Wait 24 hours or call bank' },
  '91': { responseCode: '91', category: 'SYSTEM_ERROR', description: 'Issuer switch / network node unavailable or timeout', isRetryable: true, actionRequired: 'Retry after 30 seconds with exponential backoff' },
  '96': { responseCode: '96', category: 'SYSTEM_ERROR', description: 'System malfunction / cryptographic MAC verification error', isRetryable: true, actionRequired: 'Retry after clearing security cache' }
};

export class Iso8583ResponseMapper {
  public static mapResponse(code: string): IsoResponseCodeDefinition {
    return ISO8583_RESPONSE_CODES[code] || {
      responseCode: code,
      category: 'DECLINED',
      description: `Unknown response code: ${code}`,
      isRetryable: false,
      actionRequired: 'Request alternative payment method'
    };
  }
}
""")

    # 2. Inventory Automated Packaging Cartonization Selection Matrix
    write_file("services/inventory-service/src/domain/cartonization-matrix.ts", """import { Dimensions3D } from '@novacommerce/core-types';

export interface PackagingBoxDefinition {
  boxId: string;
  name: string;
  dimensionsMm: Dimensions3D;
  tareWeightGrams: number;
  maxWeightGrams: number;
  costCents: number;
}

export const STANDARD_PACKAGING_BOXES: PackagingBoxDefinition[] = [
  { boxId: 'BOX-SMALL', name: 'Small Mailer Box', dimensionsMm: { length: 200, width: 150, height: 100 }, tareWeightGrams: 120, maxWeightGrams: 3000, costCents: 65 },
  { boxId: 'BOX-MEDIUM', name: 'Standard Medium Carton', dimensionsMm: { length: 350, width: 250, height: 180 }, tareWeightGrams: 280, maxWeightGrams: 10000, costCents: 110 },
  { boxId: 'BOX-LARGE', name: 'Large Master Carton', dimensionsMm: { length: 500, width: 400, height: 300 }, tareWeightGrams: 550, maxWeightGrams: 25000, costCents: 185 },
  { boxId: 'BOX-XLARGE', name: 'Extra Large Heavy Freight Box', dimensionsMm: { length: 800, width: 600, height: 500 }, tareWeightGrams: 1200, maxWeightGrams: 45000, costCents: 340 }
];

export class CartonizationSelector {
  public static selectBestBox(requiredLengthMm: number, requiredWidthMm: number, requiredHeightMm: number, totalWeightGrams: number): PackagingBoxDefinition | null {
    // Sort boxes by smallest volume that satisfies constraints
    const sorted = [...STANDARD_PACKAGING_BOXES].sort((a, b) => {
      const volA = a.dimensionsMm.length * a.dimensionsMm.width * a.dimensionsMm.height;
      const volB = b.dimensionsMm.length * b.dimensionsMm.width * b.dimensionsMm.height;
      return volA - volB;
    });

    for (const box of sorted) {
      const dims = [box.dimensionsMm.length, box.dimensionsMm.width, box.dimensionsMm.height].sort((a, b) => b - a);
      const req = [requiredLengthMm, requiredWidthMm, requiredHeightMm].sort((a, b) => b - a);

      if (dims[0] >= req[0] && dims[1] >= req[1] && dims[2] >= req[2] && box.maxWeightGrams >= totalWeightGrams) {
        return box;
      }
    }

    return null; // Requires custom crating or palletization
  }
}
""")

    print("Titan expansion modules generated.")

if __name__ == "__main__":
    generate_titan_expansion_modules()
