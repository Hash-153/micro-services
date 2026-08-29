export class TariffMigrationFormatter {
  public static generateCreateTableSql(): string {
    return `
      CREATE TABLE IF NOT EXISTS payment_commodity_codes (
        category_slug VARCHAR(64) PRIMARY KEY,
        unspsc_code VARCHAR(16) NOT NULL,
        description VARCHAR(255) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_payment_commodity_unspsc ON payment_commodity_codes(unspsc_code);
    `;
  }
}
