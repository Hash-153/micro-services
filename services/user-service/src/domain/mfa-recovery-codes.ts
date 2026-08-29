export class MfaRecoveryCodesGenerator {
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
