export interface DeviceFingerprintData {
  ipAddress: string;
  userAgent: string;
  acceptLanguage?: string;
  screenResolution?: string;
  timezoneOffset?: number;
  canvasHash?: string;
}

export interface AnomalyEvaluationResult {
  riskScore: number; // 0 to 100
  isSuspicious: boolean;
  requiresStepUpAuth: boolean;
  detectedAnomalies: string[];
}

export class DeviceFingerprintService {
  public static evaluateLoginAnomaly(
    current: DeviceFingerprintData,
    historicalLogins: DeviceFingerprintData[]
  ): AnomalyEvaluationResult {
    const anomalies: string[] = [];
    let riskScore = 0;

    if (historicalLogins.length === 0) {
      return {
        riskScore: 10,
        isSuspicious: false,
        requiresStepUpAuth: false,
        detectedAnomalies: ['First-time device login']
      };
    }

    const matchedIp = historicalLogins.some(h => h.ipAddress === current.ipAddress);
    const matchedUserAgent = historicalLogins.some(h => h.userAgent === current.userAgent);

    if (!matchedIp) {
      riskScore += 25;
      anomalies.push('Unrecognized IP address');
    }

    if (!matchedUserAgent) {
      riskScore += 35;
      anomalies.push('Unrecognized browser or device user-agent');
    }

    const isSuspicious = riskScore >= 50;
    const requiresStepUpAuth = riskScore >= 35;

    return {
      riskScore,
      isSuspicious,
      requiresStepUpAuth,
      detectedAnomalies: anomalies
    };
  }
}
