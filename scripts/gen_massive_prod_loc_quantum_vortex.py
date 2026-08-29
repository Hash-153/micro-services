import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_vortex_modules():
    print("Generating comprehensive Quantum Vortex Modules...")

    # 1. Payment PCI-DSS Audit Log Encryptor
    write_file("services/payment-service/src/domain/pci-audit-log-encryptor.ts", """import crypto from 'crypto';

export class PciAuditLogEncryptor {
  public static encryptLogPayload(plainTextJson: string, masterKeyHex: string): { ivHex: string; encryptedDataHex: string; authTagHex: string } {
    const key = Buffer.from(masterKeyHex, 'hex');
    const iv = crypto.randomBytes(12); // 96-bit IV for AES-GCM
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

    let encrypted = cipher.update(plainTextJson, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag();

    return {
      ivHex: iv.toString('hex'),
      encryptedDataHex: encrypted,
      authTagHex: authTag.toString('hex')
    };
  }

  public static decryptLogPayload(encryptedDataHex: string, ivHex: string, authTagHex: string, masterKeyHex: string): string {
    const key = Buffer.from(masterKeyHex, 'hex');
    const iv = Buffer.from(ivHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');

    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encryptedDataHex, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}
""")

    # 2. Inventory RFID Gate RSSI Noise Filter
    write_file("services/inventory-service/src/domain/rfid-rssi-filter.ts", """export interface RawRfidRead {
  epcTag: string;
  antennaId: number;
  rssiDecibels: number;
  timestamp: number;
}

export class RfidRssiFilter {
  public static filterMovingTag(reads: RawRfidRead[], minRssi: number = -65, minReadCount: number = 3): RawRfidRead[] {
    const grouped = new Map<string, RawRfidRead[]>();

    for (const r of reads) {
      if (r.rssiDecibels >= minRssi) {
        if (!grouped.has(r.epcTag)) {
          grouped.set(r.epcTag, []);
        }
        grouped.get(r.epcTag)!.push(r);
      }
    }

    const confirmed: RawRfidRead[] = [];
    for (const [tag, tagReads] of grouped.entries()) {
      if (tagReads.length >= minReadCount) {
        // Return latest read
        confirmed.push(tagReads[tagReads.length - 1]);
      }
    }

    return confirmed;
  }
}
""")

    print("Quantum vortex modules generated.")

if __name__ == "__main__":
    generate_quantum_vortex_modules()
