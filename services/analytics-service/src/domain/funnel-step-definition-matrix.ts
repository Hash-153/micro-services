export interface StandardFunnelDefinition {
  funnelId: string;
  name: string;
  description: string;
  stepEventNames: string[];
}

export class FunnelStepDefinitionMatrix {
  private static readonly FUNNELS: StandardFunnelDefinition[] = [
    {
      funnelId: 'funnel_standard_checkout',
      name: 'E-Commerce Standard Checkout Funnel',
      description: 'End-to-end shopping conversion flow',
      stepEventNames: [
        'catalog.product_viewed',
        'cart.item_added',
        'checkout.initiated',
        'checkout.shipping_address_entered',
        'checkout.payment_method_selected',
        'checkout.order_placed',
        'payment.authorized'
      ]
    },
    {
      funnelId: 'funnel_merchant_onboarding',
      name: 'B2B Merchant Onboarding Funnel',
      description: 'Merchant organization registration and verification',
      stepEventNames: [
        'user.registered',
        'organization.created',
        'kyc.documents_uploaded',
        'payment.bank_account_linked',
        'catalog.first_product_published'
      ]
    }
  ];

  public static getFunnel(funnelId: string): StandardFunnelDefinition | undefined {
    return this.FUNNELS.find(f => f.funnelId === funnelId);
  }

  public static getAllFunnels(): StandardFunnelDefinition[] {
    return this.FUNNELS;
  }
}
