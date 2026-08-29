export interface IsoResponseCodeDefinition {
  responseCode: string;
  category: 'APPROVED' | 'DECLINED' | 'CALL_ISSUER' | 'FRAUD_SUSPECT' | 'SYSTEM_ERROR';
  description: string;
  isRetryable: boolean;
  actionRequired: string;
}

export const ISO8583_RESPONSE_CODES: Record<string, IsoResponseCodeDefinition> = {
  '00': { responseCode: '00', category: 'APPROVED', description: 'Approved and completed successfully', isRetryable: false, actionRequired: 'Proceed with order capture' },
  '01': { responseCode: '01', category: 'CALL_ISSUER', description: 'Refer to card issuer for voice authorization', isRetryable: false, actionRequired: 'Customer must contact their issuing bank' },
  '04': { responseCode: '04', category: 'FRAUD_SUSPECT', description: 'Pick up card (fraud suspect / stolen card)', isRetryable: false, actionRequired: 'Block account and cancel transaction immediately' },
  '05': { responseCode: '05', category: 'DECLINED', description: 'Do not honor (general decline by bank risk engine)', isRetryable: false, actionRequired: 'Request an alternative payment method' },
  '12': { responseCode: '12', category: 'SYSTEM_ERROR', description: 'Invalid transaction structure or missing field', isRetryable: false, actionRequired: 'Inspect payload validation rules' },
  '14': { responseCode: '14', category: 'DECLINED', description: 'Invalid card number (no such PAN on file)', isRetryable: false, actionRequired: 'Prompt user to re-enter card details' },
  '51': { responseCode: '51', category: 'DECLINED', description: 'Insufficient funds / credit limit exceeded', isRetryable: true, actionRequired: 'Prompt user to use alternative card' },
  '54': { responseCode: '54', category: 'DECLINED', description: 'Expired card', isRetryable: false, actionRequired: 'Prompt user to update expiration date' },
  '57': { responseCode: '57', category: 'DECLINED', description: 'Transaction not permitted to cardholder (e.g. cross-border restriction)', isRetryable: false, actionRequired: 'Customer must enable international transactions' },
  '65': { responseCode: '65', category: 'DECLINED', description: 'Activity count limit exceeded (daily velocity)', isRetryable: true, actionRequired: 'Wait 24 hours or call bank' },
  '91': { responseCode: '91', category: 'SYSTEM_ERROR', description: 'Issuer switch / network node unavailable or timeout', isRetryable: true, actionRequired: 'Retry after 30 seconds with exponential backoff' },
  '96': { responseCode: '96', category: 'SYSTEM_ERROR', description: 'System malfunction / cryptographic MAC verification error', isRetryable: true, actionRequired: 'Retry after clearing security cache' }
};

export class Iso8583ResponseMapper {
  public static mapResponse(code: string): IsoResponseCodeDefinition {
    return ISO8583_RESPONSE_CODES[code] || {
      responseCode: code,
      category: 'DECLINED',
      description: `Unknown response code: ${code}`,
      isRetryable: false,
      actionRequired: 'Request alternative payment method'
    };
  }
}
