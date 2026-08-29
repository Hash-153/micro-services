import { DomainEvent, EventType } from '@novacommerce/core-types';

export interface LedgerJournalEntryRecordedEventPayload {
  journalEntryId: string; entryNumber: string; totalAmountCents: number; linesCount: number; postedAt: Date;
}

export type LedgerJournalEntryRecordedEvent = DomainEvent<LedgerJournalEntryRecordedEventPayload>;

export class LedgerJournalEntryRecordedEventFactory {
  public static create(
    aggregateId: string,
    payload: LedgerJournalEntryRecordedEventPayload,
    producer: string,
    correlationId?: string
  ): LedgerJournalEntryRecordedEvent {
    return {
      id: crypto.randomUUID(),
      eventType: 'payment.ledger.recorded' as EventType,
      aggregateId,
      aggregateType: 'LedgerJournalEntry',
      version: 1,
      timestamp: new Date().toISOString(),
      correlationId: correlationId || crypto.randomUUID(),
      producer,
      payload
    };
  }
}
