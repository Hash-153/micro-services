import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v32():
    print("Generating comprehensive Production V32 Modules...")

    # 1. Payment ISO 20022 PAIN.002 Payment Status Report Parser
    write_file("services/payment-service/src/domain/iso20022-pain002-parser.ts", """export interface PaymentStatusReport {
  originalMessageId: string;
  originalInstructionId: string;
  transactionStatus: 'ACTC' | 'ACCP' | 'RJCT' | 'PDNG';
  reasonCode?: string;
  additionalInfo?: string;
}

export class Iso20022Pain002Parser {
  public static parseStatusReport(xmlContent: string): PaymentStatusReport {
    const msgIdMatch = xmlContent.match(/<OrgnlMsgId>([^<]+)<\/OrgnlMsgId>/);
    const instrIdMatch = xmlContent.match(/<OrgnlInstrId>([^<]+)<\/OrgnlInstrId>/);
    const statusMatch = xmlContent.match(/<TxSts>([A-Z]+)<\/TxSts>/);
    const rsnMatch = xmlContent.match(/<Cd>([A-Z0-9]+)<\/Cd>/);

    return {
      originalMessageId: msgIdMatch ? msgIdMatch[1] : 'UNKNOWN_MSG',
      originalInstructionId: instrIdMatch ? instrIdMatch[1] : 'UNKNOWN_INSTR',
      transactionStatus: (statusMatch ? statusMatch[1] : 'PDNG') as PaymentStatusReport['transactionStatus'],
      reasonCode: rsnMatch ? rsnMatch[1] : undefined
    };
  }
}
""")

    # 2. Inventory Multi-Facility Load Balancer
    write_file("services/inventory-service/src/domain/facility-load-balancer.ts", """export interface FacilityCapacitySnapshot {
  warehouseId: string;
  currentActivePicksCount: number;
  maxPickThroughputPerHour: number;
  utilizationPercentage: number;
}

export class FacilityLoadBalancer {
  public static selectLeastLoadedFacility(facilities: FacilityCapacitySnapshot[]): FacilityCapacitySnapshot | null {
    if (facilities.length === 0) return null;

    return [...facilities].sort((a, b) => {
      // Choose lowest utilization percentage
      return a.utilizationPercentage - b.utilizationPercentage;
    })[0];
  }
}
""")

    print("Production V32 modules generated.")

if __name__ == "__main__":
    generate_prod_v32()
