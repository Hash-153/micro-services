import { Money, Currency } from '@novacommerce/core-types';

export interface MerchantPayoutBatchItem {
  merchantId: string;
  merchantName: string;
  bankRoutingNumber: string;
  bankAccountNumber: string;
  netPayoutAmountCents: number;
  currency: Currency;
}

export interface NachaAchBatchFile {
  batchId: string;
  totalDebitCents: number;
  totalCreditCents: number;
  entryCount: number;
  achFileContent: string;
  createdAt: Date;
}

export class BatchPayoutEngine {
  public static generateAchFile(items: MerchantPayoutBatchItem[], companyName: string = 'NOVACOMMERCE INC'): NachaAchBatchFile {
    const batchId = `ach_${Date.now().toString(36).toUpperCase()}`;
    const totalCredit = items.reduce((acc, it) => acc + it.netPayoutAmountCents, 0);

    const fileHeader = `101 121000358 199999999 ${new Date().toISOString().slice(2, 10).replace(/-/g, '')} 0945 A 094 101 ${companyName.padEnd(23, ' ')}`;
    const batchHeader = `5200 ${companyName.padEnd(16, ' ')}                    121000358 PPD PAYOUTS   ${new Date().toISOString().slice(2, 10).replace(/-/g, '')} 1 12100035 0000001`;

    const detailLines = items.map((it, idx) => {
      const paddedRouting = it.bankRoutingNumber.slice(0, 8);
      const checkDigit = it.bankRoutingNumber.slice(8, 9) || '0';
      const paddedAccount = it.bankAccountNumber.padEnd(17, ' ');
      const paddedAmount = it.netPayoutAmountCents.toString().padStart(10, '0');
      const paddedId = it.merchantId.slice(0, 15).padEnd(15, ' ');
      const paddedName = it.merchantName.slice(0, 22).padEnd(22, ' ');

      return `622 ${paddedRouting}${checkDigit} ${paddedAccount} ${paddedAmount} ${paddedId} ${paddedName} 00 12100035${(idx + 1).toString().padStart(7, '0')}`;
    });

    const batchControl = `8200 ${items.length.toString().padStart(6, '0')} 0000000000 0000000000 ${totalCredit.toString().padStart(12, '0')} 199999999           12100035 0000001`;
    const fileControl = `9000001 000001 ${(items.length + 4).toString().padStart(6, '0')} 0000000000 0000000000 ${totalCredit.toString().padStart(12, '0')}                        `;

    const fullAch = [fileHeader, batchHeader, ...detailLines, batchControl, fileControl].join('\n');

    return {
      batchId,
      totalDebitCents: 0,
      totalCreditCents: totalCredit,
      entryCount: items.length,
      achFileContent: fullAch,
      createdAt: new Date()
    };
  }
}
