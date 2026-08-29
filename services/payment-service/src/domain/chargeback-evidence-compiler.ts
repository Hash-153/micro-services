export interface EvidenceAttachment {
  type: 'RECEIPT' | 'PROOF_OF_DELIVERY' | 'TERMS_AND_CONDITIONS' | 'CUSTOMER_COMMUNICATION' | 'REFUND_POLICY';
  fileKey: string;
  mimeType: string;
  sha256Checksum: string;
}

export interface DisputeDefensePackage {
  disputeId: string;
  orderNumber: string;
  defenseExplanation: string;
  attachments: EvidenceAttachment[];
  customerSignatureTimestamp?: string;
  carrierDeliveryGpsLocation?: string;
}

export class ChargebackEvidenceCompiler {
  public static compilePackage(
    disputeId: string,
    orderNumber: string,
    customerName: string,
    trackingNumber: string,
    deliveryDate: string,
    attachments: EvidenceAttachment[]
  ): DisputeDefensePackage {
    const defenseExplanation = `Order #${orderNumber} was purchased by ${customerName} with 3D Secure authentication. Goods were successfully fulfilled and delivered via carrier tracking #${trackingNumber} on ${deliveryDate}.`;

    return {
      disputeId,
      orderNumber,
      defenseExplanation,
      attachments
    };
  }
}
