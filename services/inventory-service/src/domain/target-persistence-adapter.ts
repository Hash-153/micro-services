export class TargetPersistenceAdapter {
  public static generateUpdateSql(targets: { sku: string; targetUnits: number }[]): string[] {
    return targets.map(
      t => `UPDATE inventory_safety_stocks SET safety_stock_threshold = ${t.targetUnits}, updated_at = NOW() WHERE sku = '${t.sku}';`
    );
  }
}
