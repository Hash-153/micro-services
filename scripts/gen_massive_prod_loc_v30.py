import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v30():
    print("Generating comprehensive Production V30 Modules...")

    # 1. Payment ISO 20022 CAMT.053 Bank Statement Reconciliation Parser
    write_file("services/payment-service/src/domain/iso20022-camt053-parser.ts", """export interface BankStatementEntry {
  entryReference: string;
  amountCents: number;
  creditDebitIndicator: 'CRDT' | 'DBIT';
  bookingDate: Date;
  valueDate: Date;
  proprietaryCode: string;
  remittanceText?: string;
}

export class Iso20022Camt053Parser {
  public static parseStatementEntries(xmlStatement: string): BankStatementEntry[] {
    const entries: BankStatementEntry[] = [];
    const entryBlocks = xmlStatement.split('<Ntry>');

    for (let i = 1; i < entryBlocks.length; i++) {
      const block = entryBlocks[i].split('</Ntry>')[0];
      const amtMatch = block.match(/<Amt[^>]*>([0-9.]+)<\/Amt>/);
      const cdtDbtMatch = block.match(/<CdtDbtInd>([A-Z]+)<\/CdtDbtInd>/);
      const refMatch = block.match(/<AcctSvcrRef>([^<]+)<\/AcctSvcrRef>/);

      if (amtMatch && cdtDbtMatch) {
        entries.push({
          entryReference: refMatch ? refMatch[1] : `REF-${i}`,
          amountCents: Math.round(parseFloat(amtMatch[1]) * 100),
          creditDebitIndicator: cdtDbtMatch[1] as 'CRDT' | 'DBIT',
          bookingDate: new Date(),
          valueDate: new Date(),
          proprietaryCode: 'NTRF'
        });
      }
    }

    return entries;
  }
}
""")

    # 2. Fulfillment Hazmat Packaging Compliance Checker
    write_file("services/fulfillment-service/src/domain/hazmat-compliance-checker.ts", """export interface HazmatMaterialSpec {
  unNumber: string; // e.g. "UN3481" for Lithium ion batteries packed with equipment
  properShippingName: string;
  hazardClass: string; // e.g. "Class 9"
  packingGroup: 'I' | 'II' | 'III';
  maxNetQuantityGrams: number;
}

export class HazmatComplianceChecker {
  private static readonly REGULATED_MATERIALS: Map<string, HazmatMaterialSpec> = new Map([
    ['UN3480', { unNumber: 'UN3480', properShippingName: 'Lithium Ion Batteries', hazardClass: '9', packingGroup: 'II', maxNetQuantityGrams: 5000 }],
    ['UN3481', { unNumber: 'UN3481', properShippingName: 'Lithium Ion Batteries Packed with Equipment', hazardClass: '9', packingGroup: 'II', maxNetQuantityGrams: 10000 }],
    ['UN1993', { unNumber: 'UN1993', properShippingName: 'Flammable Liquids N.O.S. (Cleaning Solvents)', hazardClass: '3', packingGroup: 'III', maxNetQuantityGrams: 1000 }]
  ]);

  public static checkCompliance(unNumber: string, netWeightGrams: number): { isAllowed: boolean; reason?: string; requiredLabel: string } {
    const spec = this.REGULATED_MATERIALS.get(unNumber);
    if (!spec) {
      return { isAllowed: false, reason: `Unknown or uncertified hazmat material: ${unNumber}`, requiredLabel: 'NONE' };
    }

    if (netWeightGrams > spec.maxNetQuantityGrams) {
      return {
        isAllowed: false,
        reason: `Net quantity (${netWeightGrams}g) exceeds allowable limit for ${unNumber} (${spec.maxNetQuantityGrams}g)`,
        requiredLabel: `HAZMAT_CLASS_${spec.hazardClass.replace(/\\s/g, '_')}`
      };
    }

    return {
      isAllowed: true,
      requiredLabel: `HAZMAT_CLASS_${spec.hazardClass.replace(/\\s/g, '_')}_LABEL`
    };
  }
}
""")

    print("Production V30 modules generated.")

if __name__ == "__main__":
    generate_prod_v30()
