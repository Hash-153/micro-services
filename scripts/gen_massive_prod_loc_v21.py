import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v21():
    print("Generating comprehensive Production V21 Modules...")

    # 1. Catalog Multi-Language Translation Fallback Engine
    write_file("services/catalog-service/src/domain/catalog-i18n-resolver.ts", """export interface LocalizedContent {
  locale: string; // e.g. "en-US", "fr-FR", "es-ES", "de-DE", "ja-JP"
  title: string;
  description: string;
  bulletPoints: string[];
}

export class CatalogI18nResolver {
  public static resolve(
    translations: LocalizedContent[],
    preferredLocale: string = 'en-US',
    defaultLocale: string = 'en-US'
  ): LocalizedContent {
    const exact = translations.find(t => t.locale.toLowerCase() === preferredLocale.toLowerCase());
    if (exact) return exact;

    // Try language prefix match (e.g. "fr" from "fr-CA")
    const langPrefix = preferredLocale.split('-')[0].toLowerCase();
    const langMatch = translations.find(t => t.locale.toLowerCase().startsWith(langPrefix));
    if (langMatch) return langMatch;

    // Fallback to default
    const def = translations.find(t => t.locale.toLowerCase() === defaultLocale.toLowerCase());
    if (def) return def;

    // Fallback to first available
    return translations[0] || {
      locale: defaultLocale,
      title: '',
      description: '',
      bulletPoints: []
    };
  }
}
""")

    # 2. Fulfillment Multi-Carrier Tracking Milestone Aggregator
    write_file("services/fulfillment-service/src/domain/tracking-milestone-aggregator.ts", """import { FulfillmentStatus, CarrierCode } from '@novacommerce/core-types';

export interface TrackingMilestone {
  timestamp: Date;
  status: FulfillmentStatus;
  description: string;
  locationCity?: string;
  locationState?: string;
  locationCountry?: string;
}

export class TrackingMilestoneAggregator {
  public static sortAndDeduplicate(milestones: TrackingMilestone[]): TrackingMilestone[] {
    const sorted = [...milestones].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

    const deduplicated: TrackingMilestone[] = [];
    for (const m of sorted) {
      const isDuplicate = deduplicated.some(
        d => d.status === m.status && Math.abs(new Date(d.timestamp).getTime() - new Date(m.timestamp).getTime()) < 60000
      );
      if (!isDuplicate) {
        deduplicated.push(m);
      }
    }

    return deduplicated;
  }
}
""")

    print("Production V21 modules generated.")

if __name__ == "__main__":
    generate_prod_v21()
