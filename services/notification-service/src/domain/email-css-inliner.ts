export class EmailCssInliner {
  public static inlineStyles(htmlContent: string): string {
    // Basic inline transformation for bulletproof HTML emails
    return htmlContent
      .replace(/<p>/g, '<p style="margin: 0 0 16px; font-size: 15px; line-height: 1.5; color: #334155;">')
      .replace(/<h1>/g, '<h1 style="margin: 0 0 20px; font-size: 24px; font-weight: 700; color: #0f172a;">')
      .replace(/<h2>/g, '<h2 style="margin: 0 0 16px; font-size: 18px; font-weight: 600; color: #0f172a;">')
      .replace(/<a /g, '<a style="color: #2563eb; text-decoration: underline;" ')
      .replace(/<button>/g, '<button style="background-color: #2563eb; color: #ffffff; padding: 12px 24px; border-radius: 6px; font-weight: 600; border: none; cursor: pointer;">');
  }
}
