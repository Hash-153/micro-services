export interface UpiIntentUrlParameters {
  vpa: string; // Virtual Payment Address (e.g. merchant@icici)
  payeeName: string;
  transactionRef: string; // Unique transaction reference (tr)
  orderId: string;
  amount: number; // in INR
  currency: 'INR';
  transactionNote: string;
}

export class UpiPaymentEngine {
  public static generateIntentUrl(params: UpiIntentUrlParameters): string {
    const encodedName = encodeURIComponent(params.payeeName);
    const encodedNote = encodeURIComponent(params.transactionNote);
    const formattedAmount = params.amount.toFixed(2);

    return `upi://pay?pa=${params.vpa}&pn=${encodedName}&mc=5311&tr=${params.transactionRef}&tid=${params.transactionRef}&am=${formattedAmount}&cu=INR&url=https://novacommerce.io&tn=${encodedNote}`;
  }

  public static parseUpiCallback(queryUrl: string): { status: 'SUCCESS' | 'FAILURE' | 'PENDING'; txnId?: string; responseCode?: string } {
    const params = new URLSearchParams(queryUrl);
    const status = params.get('Status') || params.get('status');
    const txnId = params.get('txnId') || params.get('txnRef') || undefined;
    const responseCode = params.get('responseCode') || undefined;

    if (status === 'SUCCESS' || responseCode === '00') {
      return { status: 'SUCCESS', txnId, responseCode };
    }
    if (status === 'SUBMITTED' || status === 'PENDING') {
      return { status: 'PENDING', txnId, responseCode };
    }
    return { status: 'FAILURE', txnId, responseCode };
  }
}
