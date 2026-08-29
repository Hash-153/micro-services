export interface HsTariffClassification {
  hsChapter: string;
  hsHeading: string;
  hsSubheading: string;
  fullTariffCode: string;
  description: string;
  dutyRateGeneralPercent: number;
  isSpecialPermitRequired: boolean;
}

export const GLOBAL_HS_TARIFF_SCHEDULE: HsTariffClassification[] = [
  { hsChapter: '84', hsHeading: '8471', hsSubheading: '847130', fullTariffCode: '8471.30.0100', description: 'Portable automatic data processing machines, weighing not more than 10 kg, consisting of at least a central processing unit, a keyboard and a display', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '84', hsHeading: '8471', hsSubheading: '847141', fullTariffCode: '8471.41.0150', description: 'Other automatic data processing machines comprising in the same housing at least a central processing unit and an input and output unit', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '84', hsHeading: '8471', hsSubheading: '847150', fullTariffCode: '8471.50.0150', description: 'Digital processing units other than those of subheading 8471.41 or 8471.49, whether or not containing in the same housing one or two of the following types of unit: storage units, input units, output units', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '84', hsHeading: '8471', hsSubheading: '847170', fullTariffCode: '8471.70.4065', description: 'Solid-state non-volatile storage devices (Flash memory cards, SSDs, NVMe drives)', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '85', hsHeading: '8517', hsSubheading: '851762', fullTariffCode: '8517.62.0050', description: 'Machines for the reception, conversion and transmission or regeneration of voice, images or other data, including switching and routing apparatus', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '85', hsHeading: '8504', hsSubheading: '850440', fullTariffCode: '8504.40.7007', description: 'Static converters: Power supplies suitable for physical incorporation into automatic data processing machines or units thereof', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '85', hsHeading: '8528', hsSubheading: '852852', fullTariffCode: '8528.52.0000', description: 'Monitors capable of directly connecting to and designed for use with an automatic data processing machine of heading 8471', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '85', hsHeading: '8542', hsSubheading: '854231', fullTariffCode: '8542.31.0000', description: 'Electronic integrated circuits: Processors and controllers, whether or not combined with memories, converters, logic circuits, amplifiers, clock and timing circuits, or other circuits', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '85', hsHeading: '8542', hsSubheading: '854232', fullTariffCode: '8542.32.0015', description: 'Electronic integrated circuits: Memories - Dynamic read-write random access memories (DRAM) and NAND flash memories', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false },
  { hsChapter: '85', hsHeading: '8544', hsSubheading: '854470', fullTariffCode: '8544.70.0000', description: 'Optical fiber cables made up of individually sheathed fibers, whether or not assembled with electric conductors or fitted with connectors', dutyRateGeneralPercent: 0.0, isSpecialPermitRequired: false }
];

export class HsTariffLookupEngine {
  public static classifyItem(productDescription: string): HsTariffClassification {
    const lower = productDescription.toLowerCase();
    if (lower.includes('switch') || lower.includes('router') || lower.includes('firewall')) {
      return GLOBAL_HS_TARIFF_SCHEDULE[4];
    }
    if (lower.includes('ssd') || lower.includes('nvme') || lower.includes('flash')) {
      return GLOBAL_HS_TARIFF_SCHEDULE[3];
    }
    if (lower.includes('server') || lower.includes('rack') || lower.includes('blade')) {
      return GLOBAL_HS_TARIFF_SCHEDULE[2];
    }
    if (lower.includes('monitor') || lower.includes('display')) {
      return GLOBAL_HS_TARIFF_SCHEDULE[6];
    }
    if (lower.includes('gpu') || lower.includes('cpu') || lower.includes('processor')) {
      return GLOBAL_HS_TARIFF_SCHEDULE[7];
    }
    return GLOBAL_HS_TARIFF_SCHEDULE[0]; // Default portable laptop/workstation
  }
}
