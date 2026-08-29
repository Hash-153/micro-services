export interface BmcManagementCardSpecConfig {
  specId: string;
  categorySlug: 'bmc-management-card';
  categoryName: 'OpenBMC AST2600 Remote Out-of-Band Controllers';
  hardwareDomain: 'Compute';
  supportedVendorArchitectures: string[];
  powerConsumptionWatts: { idle: number; typical: number; maxPeak: number };
  environmentalSpecs: { minOperatingTempCelsius: number; maxOperatingTempCelsius: number; maxHumidityPercent: number };
  mtbfHours: number;
  warrantyPeriodMonths: number;
  certifications: string[];
  manufacturingTolerances: { dimensionalToleranceMm: number; weightToleranceGrams: number };
  lifecycleStatus: 'GA' | 'END_OF_SALE' | 'END_OF_LIFE' | 'EARLY_ACCESS';
}

export const BMC_MANAGEMENT_CARD_DEFAULT_SPEC: BmcManagementCardSpecConfig = {
  specId: 'spec_bmc-management-card_v1',
  categorySlug: 'bmc-management-card',
  categoryName: 'OpenBMC AST2600 Remote Out-of-Band Controllers',
  hardwareDomain: 'Compute',
  supportedVendorArchitectures: ['x86_64', 'ARM64_Neoverse', 'RISC-V_Enterprise', 'OpenPOWER'],
  powerConsumptionWatts: { idle: 250, typical: 850, maxPeak: 1600 },
  environmentalSpecs: { minOperatingTempCelsius: 10, maxOperatingTempCelsius: 35, maxHumidityPercent: 85 },
  mtbfHours: 250000,
  warrantyPeriodMonths: 36,
  certifications: ['CE', 'FCC_CLASS_A', 'UL_62368_1', 'ROHS_COMPLIANT', 'ENERGY_STAR', 'VCCI_CLASS_A', 'CB_SCHEME'],
  manufacturingTolerances: { dimensionalToleranceMm: 0.5, weightToleranceGrams: 50 },
  lifecycleStatus: 'GA'
};

export class BmcManagementCardSpecValidator {
  public static validate(config: BmcManagementCardSpecConfig): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];
    if (config.powerConsumptionWatts.maxPeak < config.powerConsumptionWatts.typical) {
      errors.push('Peak power cannot be less than typical operating power consumption');
    }
    if (config.environmentalSpecs.maxOperatingTempCelsius <= config.environmentalSpecs.minOperatingTempCelsius) {
      errors.push('Invalid thermal operating window');
    }
    if (config.warrantyPeriodMonths < 12) {
      errors.push('Enterprise hardware requires a minimum 12-month manufacturer warranty');
    }
    return { isValid: errors.length === 0, errors };
  }

  public static getDeratingCurve(ambientTempCelsius: number, config: BmcManagementCardSpecConfig = BMC_MANAGEMENT_CARD_DEFAULT_SPEC): number {
    if (ambientTempCelsius <= 25) return 1.0;
    if (ambientTempCelsius >= config.environmentalSpecs.maxOperatingTempCelsius) return 0.70;
    const delta = ambientTempCelsius - 25;
    const maxDelta = config.environmentalSpecs.maxOperatingTempCelsius - 25;
    return 1.0 - (0.30 * (delta / maxDelta));
  }
}
