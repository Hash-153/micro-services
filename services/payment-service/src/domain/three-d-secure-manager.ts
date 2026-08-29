export interface ThreeDSecureChallengeRequest {
  transactionId: string;
  amountCents: number;
  currency: string;
  cardBin: string;
  returnUrl: string;
}

export interface ThreeDSecureChallengeResponse {
  threeDSecureVersion: '2.2.0';
  acsUrl: string;
  cReqPayload: string;
  isFrictionless: boolean;
}

export class ThreeDSecureManager {
  public static initiateChallenge(request: ThreeDSecureChallengeRequest): ThreeDSecureChallengeResponse {
    const isFrictionless = request.amountCents < 5000; // < $50 frictionless exemption
    const cReq = Buffer.from(JSON.stringify({
      threeDSServerTransID: `3ds_${crypto.randomUUID()}`,
      acsTransID: `acs_${Date.now().toString(36)}`,
      challengeWindowSize: '05'
    })).toString('base64');

    return {
      threeDSecureVersion: '2.2.0',
      acsUrl: 'https://acs.novacommerce-payments.net/challenge',
      cReqPayload: cReq,
      isFrictionless
    };
  }
}
