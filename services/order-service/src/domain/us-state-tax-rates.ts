export interface StateTaxRule {
  stateCode: string;
  stateName: string;
  baseRate: number;
  maxLocalRate: number;
  isDestinationBased: boolean;
  taxesShipping: boolean;
  taxesDigitalGoods: boolean;
  specialRules: string[];
}

export const US_STATE_TAX_RULES: Record<string, StateTaxRule> = {
  AL: { stateCode: 'AL', stateName: 'Alabama', baseRate: 0.04, maxLocalRate: 0.075, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Automotive rate cap', 'Farm machinery reduced rate'] },
  AK: { stateCode: 'AK', stateName: 'Alaska', baseRate: 0.00, maxLocalRate: 0.075, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['No state tax; local borough tax only'] },
  AZ: { stateCode: 'AZ', stateName: 'Arizona', baseRate: 0.056, maxLocalRate: 0.053, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Transaction privilege tax structure'] },
  AR: { stateCode: 'AR', stateName: 'Arkansas', baseRate: 0.065, maxLocalRate: 0.05125, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Food tax reduced to 0.125%'] },
  CA: { stateCode: 'CA', stateName: 'California', baseRate: 0.0725, maxLocalRate: 0.035, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Mandated local district tax minimum 0.25%'] },
  CO: { stateCode: 'CO', stateName: 'Colorado', baseRate: 0.029, maxLocalRate: 0.083, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Home-rule jurisdiction self-collection'] },
  CT: { stateCode: 'CT', stateName: 'Connecticut', baseRate: 0.0635, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Luxury items taxed at 7.75%'] },
  DE: { stateCode: 'DE', stateName: 'Delaware', baseRate: 0.00, maxLocalRate: 0.00, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Zero sales tax state; Gross receipts tax on seller'] },
  FL: { stateCode: 'FL', stateName: 'Florida', baseRate: 0.06, maxLocalRate: 0.025, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Discretionary sales surtax on first $5,000 only'] },
  GA: { stateCode: 'GA', stateName: 'Georgia', baseRate: 0.04, maxLocalRate: 0.05, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Local option sales tax applies'] },
  HI: { stateCode: 'HI', stateName: 'Hawaii', baseRate: 0.04, maxLocalRate: 0.005, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['General excise tax levied on gross income'] },
  ID: { stateCode: 'ID', stateName: 'Idaho', baseRate: 0.06, maxLocalRate: 0.03, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Resort cities local tax option'] },
  IL: { stateCode: 'IL', stateName: 'Illinois', baseRate: 0.0625, maxLocalRate: 0.0475, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Rotational tax threshold for remote sellers'] },
  IN: { stateCode: 'IN', stateName: 'Indiana', baseRate: 0.07, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Uniform statewide 7% without local surtaxes'] },
  IA: { stateCode: 'IA', stateName: 'Iowa', baseRate: 0.06, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Exemption for unprocessed grocery foods'] },
  KS: { stateCode: 'KS', stateName: 'Kansas', baseRate: 0.065, maxLocalRate: 0.04, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Food tax phased reductions'] },
  KY: { stateCode: 'KY', stateName: 'Kentucky', baseRate: 0.06, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Single state tax rate; no local add-ons'] },
  LA: { stateCode: 'LA', stateName: 'Louisiana', baseRate: 0.0445, maxLocalRate: 0.07, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Parish level independent tax authorities'] },
  ME: { stateCode: 'ME', stateName: 'Maine', baseRate: 0.055, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Prepared food taxed at 8%; Lodging at 9%'] },
  MD: { stateCode: 'MD', stateName: 'Maryland', baseRate: 0.06, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Digital advertising tax framework'] },
  MA: { stateCode: 'MA', stateName: 'Massachusetts', baseRate: 0.0625, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Clothing under $175 is tax exempt'] },
  MI: { stateCode: 'MI', stateName: 'Michigan', baseRate: 0.06, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Uniform 6% statewide rate'] },
  MN: { stateCode: 'MN', stateName: 'Minnesota', baseRate: 0.06875, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['General apparel is completely exempt from sales tax'] },
  MS: { stateCode: 'MS', stateName: 'Mississippi', baseRate: 0.07, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Strict 7% baseline across tangible personal property'] },
  MO: { stateCode: 'MO', stateName: 'Missouri', baseRate: 0.04225, maxLocalRate: 0.05763, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Complex local taxing district boundaries'] },
  MT: { stateCode: 'MT', stateName: 'Montana', baseRate: 0.00, maxLocalRate: 0.03, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['No statewide sales tax; local resort tax permitted'] },
  NE: { stateCode: 'NE', stateName: 'Nebraska', baseRate: 0.055, maxLocalRate: 0.025, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Municipal sales tax additions'] },
  NV: { stateCode: 'NV', stateName: 'Nevada', baseRate: 0.0685, maxLocalRate: 0.01525, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Clark County higher rate for public transit'] },
  NH: { stateCode: 'NH', stateName: 'New Hampshire', baseRate: 0.00, maxLocalRate: 0.00, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['No general sales tax; meals and rooms taxed at 8.5%'] },
  NJ: { stateCode: 'NJ', stateName: 'New Jersey', baseRate: 0.06625, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Urban enterprise zones offer 3.3125% rate'] },
  NM: { stateCode: 'NM', stateName: 'New Mexico', baseRate: 0.04875, maxLocalRate: 0.04188, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Gross receipts tax applies to goods and services'] },
  NY: { stateCode: 'NY', stateName: 'New York', baseRate: 0.04, maxLocalRate: 0.04875, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Clothing and footwear under $110 exempt from state tax'] },
  NC: { stateCode: 'NC', stateName: 'North Carolina', baseRate: 0.0475, maxLocalRate: 0.0275, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Counties levy 2% or 2.25% add-on rates'] },
  ND: { stateCode: 'ND', stateName: 'North Dakota', baseRate: 0.05, maxLocalRate: 0.035, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Farm machinery special lower bracket'] },
  OH: { stateCode: 'OH', stateName: 'Ohio', baseRate: 0.0575, maxLocalRate: 0.0225, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Transit authority and county add-on taxes'] },
  OK: { stateCode: 'OK', stateName: 'Oklahoma', baseRate: 0.045, maxLocalRate: 0.07, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['High variance in municipal sales taxes'] },
  OR: { stateCode: 'OR', stateName: 'Oregon', baseRate: 0.00, maxLocalRate: 0.00, isDestinationBased: false, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Zero sales tax state; Corporate activity tax on receipts'] },
  PA: { stateCode: 'PA', stateName: 'Pennsylvania', baseRate: 0.06, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Allegheny County 1%, Philadelphia 2% local add-on'] },
  RI: { stateCode: 'RI', stateName: 'Rhode Island', baseRate: 0.07, maxLocalRate: 0.00, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Single statewide 7% sales tax'] },
  SC: { stateCode: 'SC', stateName: 'South Carolina', baseRate: 0.06, maxLocalRate: 0.03, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Local option sales and transportation taxes'] },
  SD: { stateCode: 'SD', stateName: 'South Dakota', baseRate: 0.042, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['South Dakota v. Wayfair historic nexus state'] },
  TN: { stateCode: 'TN', stateName: 'Tennessee', baseRate: 0.07, maxLocalRate: 0.0275, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Single article tax cap structure'] },
  TX: { stateCode: 'TX', stateName: 'Texas', baseRate: 0.0625, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Cap at 8.25% maximum combined state and local'] },
  UT: { stateCode: 'UT', stateName: 'Utah', baseRate: 0.061, maxLocalRate: 0.0295, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: true, specialRules: ['Food taxed at reduced state rate of 1.75%'] },
  VT: { stateCode: 'VT', stateName: 'Vermont', baseRate: 0.06, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Local 1% option tax in select municipalities'] },
  VA: { stateCode: 'VA', stateName: 'Virginia', baseRate: 0.053, maxLocalRate: 0.017, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['Northern Virginia and Hampton Roads regional tax'] },
  WA: { stateCode: 'WA', stateName: 'Washington', baseRate: 0.065, maxLocalRate: 0.04, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['Business and Occupation (B&O) tax co-exists'] },
  WV: { stateCode: 'WV', stateName: 'West Virginia', baseRate: 0.06, maxLocalRate: 0.01, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: false, specialRules: ['Food completely exempt from state tax'] },
  WI: { stateCode: 'WI', stateName: 'Wisconsin', baseRate: 0.05, maxLocalRate: 0.009, isDestinationBased: true, taxesShipping: true, taxesDigitalGoods: true, specialRules: ['County 0.5% sales tax in majority of counties'] },
  WY: { stateCode: 'WY', stateName: 'Wyoming', baseRate: 0.04, maxLocalRate: 0.02, isDestinationBased: true, taxesShipping: false, taxesDigitalGoods: false, specialRules: ['County optional 1% general and 1% specific tax'] }
};
