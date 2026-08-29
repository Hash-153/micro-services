export interface ChargebackReasonDefinition {
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
