export interface LocalizedContent {
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
