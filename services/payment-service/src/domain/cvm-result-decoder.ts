export type CvmResultType = 'ONLINE_PIN' | 'OFFLINE_PIN' | 'SIGNATURE' | 'CONSUMER_DEVICE_CDCVM' | 'NO_CVM_REQUIRED' | 'CVM_FAILED';

export class CvmResultDecoder {
  public static decodeCvm(field55Hex: string): { cvmType: CvmResultType; isCardholderAuthenticated: boolean; description: string } {
    if (!field55Hex || field55Hex.length === 0) {
      return { cvmType: 'NO_CVM_REQUIRED', isCardholderAuthenticated: true, description: 'No CVM requested / contactless under CVM limit' };
    }

    if (field55Hex.includes('1F03') || field55Hex.includes('5F34')) {
      return { cvmType: 'CONSUMER_DEVICE_CDCVM', isCardholderAuthenticated: true, description: 'Apple Pay / Google Pay Biometric (TouchID / FaceID) on device' };
    }

    if (field55Hex.includes('8E0401') || field55Hex.includes('8E0402')) {
      return { cvmType: 'ONLINE_PIN', isCardholderAuthenticated: true, description: 'Online Encrypted PIN entered on PINpad' };
    }

    if (field55Hex.includes('8E041E')) {
      return { cvmType: 'SIGNATURE', isCardholderAuthenticated: true, description: 'Paper or electronic signature captured' };
    }

    return { cvmType: 'NO_CVM_REQUIRED', isCardholderAuthenticated: true, description: 'Standard chip processing without extra CVM step' };
  }
}
