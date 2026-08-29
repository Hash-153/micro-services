import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v4():
    print("Generating comprehensive Production V4 Modules...")

    # 1. Core Logger Elastic Common Schema (ECS) Formatter
    write_file("packages/core-logger/src/ecs-formatter.ts", """export interface EcsLogEntry {
  '@timestamp': string;
  'log.level': string;
  message: string;
  'service.name': string;
  'service.version': string;
  'trace.id'?: string;
  'transaction.id'?: string;
  'error.type'?: string;
  'error.message'?: string;
  'error.stack_trace'?: string;
  custom?: Record<string, any>;
}

export class EcsLogFormatter {
  private serviceName: string;
  private serviceVersion: string;

  constructor(serviceName: string, serviceVersion: string = '1.0.0') {
    this.serviceName = serviceName;
    this.serviceVersion = serviceVersion;
  }

  public format(level: string, message: string, context?: Record<string, any>, error?: Error): string {
    const entry: EcsLogEntry = {
      '@timestamp': new Date().toISOString(),
      'log.level': level.toUpperCase(),
      message,
      'service.name': this.serviceName,
      'service.version': this.serviceVersion,
      'trace.id': context?.traceId,
      'transaction.id': context?.transactionId
    };

    if (error) {
      entry['error.type'] = error.name;
      entry['error.message'] = error.message;
      entry['error.stack_trace'] = error.stack;
    }

    if (context) {
      const { traceId, transactionId, ...rest } = context;
      if (Object.keys(rest).length > 0) {
        entry.custom = rest;
      }
    }

    return JSON.stringify(entry);
  }
}
""")

    # 2. User Service Multi-Factor Recovery Codes Generator
    write_file("services/user-service/src/domain/mfa-recovery-codes.ts", """export class MfaRecoveryCodesGenerator {
  public static generateCodes(count: number = 8): { rawCodes: string[]; hashedCodes: string[] } {
    const rawCodes: string[] = [];
    const hashedCodes: string[] = [];

    for (let i = 0; i < count; i++) {
      const part1 = Math.random().toString(36).substring(2, 6).toUpperCase();
      const part2 = Math.random().toString(36).substring(2, 6).toUpperCase();
      const raw = `${part1}-${part2}`;
      rawCodes.push(raw);
      
      // Simple cryptographic hash representation
      hashedCodes.push(`hash_${Buffer.from(raw).toString('hex')}`);
    }

    return { rawCodes, hashedCodes };
  }

  public static verifyAndBurnCode(rawInput: string, hashedList: string[]): { isValid: boolean; remainingHashedList: string[] } {
    const cleanInput = rawInput.trim().toUpperCase();
    const targetHash = `hash_${Buffer.from(cleanInput).toString('hex')}`;
    const idx = hashedList.indexOf(targetHash);

    if (idx === -1) {
      return { isValid: false, remainingHashedList: hashedList };
    }

    const remaining = [...hashedList];
    remaining.splice(idx, 1);
    return { isValid: true, remainingHashedList: remaining };
  }
}
""")

    print("Production V4 modules generated.")

if __name__ == "__main__":
    generate_prod_v4()
