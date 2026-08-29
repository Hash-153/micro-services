export class TemplateVariableValidator {
  public static extractRequiredVariables(templateHtml: string): string[] {
    const regex = /{{\s*([a-zA-Z0-9_]+)\s*}}/g;
    const matches = new Set<string>();
    let m;
    while ((m = regex.exec(templateHtml)) !== null) {
      matches.add(m[1]);
    }
    return Array.from(matches);
  }

  public static validateVariablesSupplied(
    templateHtml: string,
    suppliedVariables: Record<string, any>
  ): { isValid: boolean; missingVariables: string[] } {
    const required = this.extractRequiredVariables(templateHtml);
    const missing: string[] = [];

    for (const v of required) {
      if (suppliedVariables[v] === undefined || suppliedVariables[v] === null) {
        missing.push(v);
      }
    }

    return {
      isValid: missing.length === 0,
      missingVariables: missing
    };
  }
}
