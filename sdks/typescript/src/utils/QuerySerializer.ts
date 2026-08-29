export class QuerySerializer {
  public static serialize(params: Record<string, any>): string {
    const searchParams = new URLSearchParams();

    for (const [key, value] of Object.entries(params)) {
      if (value === undefined || value === null || value === '') {
        continue;
      }
      if (Array.isArray(value)) {
        searchParams.append(key, value.join(','));
      } else if (typeof value === 'object' && !(value instanceof Date)) {
        searchParams.append(key, JSON.stringify(value));
      } else if (value instanceof Date) {
        searchParams.append(key, value.toISOString());
      } else {
        searchParams.append(key, String(value));
      }
    }

    const qs = searchParams.toString();
    return qs ? `?${qs}` : '';
  }
}
