import { Level3LineItemData } from './level3-card-data-builder.js';

export class LineItemDiscountDistributor {
  public static distributeDiscount(items: Level3LineItemData[], totalDiscountCents: number): Level3LineItemData[] {
    const totalGross = items.reduce((acc, it) => acc + it.totalAmountCents, 0);
    if (totalGross === 0 || totalDiscountCents <= 0) return items;

    let remainingDiscount = totalDiscountCents;
    return items.map((it, idx) => {
      if (idx === items.length - 1) {
        return {
          ...it,
          discountAmountCents: remainingDiscount
        };
      }

      const propDiscount = Math.round((it.totalAmountCents / totalGross) * totalDiscountCents);
      const allocated = Math.min(propDiscount, remainingDiscount);
      remainingDiscount -= allocated;

      return {
        ...it,
        discountAmountCents: allocated
      };
    });
  }
}
