export type CardBrand = 'VISA' | 'MASTERCARD' | 'AMEX' | 'DISCOVER' | 'JCB' | 'DINERS_CLUB' | 'UNKNOWN';

export interface CardValidationResult {
  isValidLuhn: boolean;
  brand: CardBrand;
  isSupported: boolean;
  lastFourDigits: string;
  bin: string;
}

export class LuhnCardValidator {
  public static validate(cardNumber: string): CardValidationResult {
    const cleanNumber = cardNumber.replace(/[\s-]/g, '');
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
    if (/^(?:2131|1800|35\d{3})\d{11}$/.test(numberStr)) {
      return 'JCB';
    }
    if (/^3(?:0[0-5]|[68][0-9])[0-9]{11}$/.test(numberStr)) {
      return 'DINERS_CLUB';
    }
    return 'UNKNOWN';
  }
}
