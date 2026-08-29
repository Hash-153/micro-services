export interface CategoryAttributeField {
  attributeKey: string;
  label: string;
  dataType: 'STRING' | 'NUMBER' | 'BOOLEAN' | 'ENUM';
  isRequired: boolean;
  allowedValues?: string[];
  unit?: string;
  description: string;
}

export const ENTERPRISE_CATEGORY_ATTRIBUTE_SCHEMAS: Record<string, CategoryAttributeField[]> = {
  'cat_srv_rack': [
    { attributeKey: 'formFactor', label: 'Form Factor', dataType: 'ENUM', isRequired: true, allowedValues: ['1U', '2U', '4U', '8U'], description: 'Rack unit standard sizing' },
    { attributeKey: 'cpuSockets', label: 'CPU Sockets', dataType: 'NUMBER', isRequired: true, unit: 'count', description: 'Number of LGA/SP5 processor sockets' },
    { attributeKey: 'chipsetGeneration', label: 'Chipset Generation', dataType: 'STRING', isRequired: true, description: 'Motherboard platform chipset family' },
    { attributeKey: 'maxMemoryGb', label: 'Max RAM Capacity', dataType: 'NUMBER', isRequired: true, unit: 'GB', description: 'Total DDR5 ECC Registered capacity' },
    { attributeKey: 'dimmSlots', label: 'DIMM Slots', dataType: 'NUMBER', isRequired: true, unit: 'slots', description: 'Number of memory channels and slots' },
    { attributeKey: 'pcieGen5Lanes', label: 'PCIe Gen 5 Expansion Lanes', dataType: 'NUMBER', isRequired: true, unit: 'lanes', description: 'Total PCIe 5.0 lanes' },
    { attributeKey: 'nvmeDriveBays', label: 'U.2/U.3 NVMe Hot-Swap Bays', dataType: 'NUMBER', isRequired: true, unit: 'bays', description: 'Front-accessible direct attach bays' },
    { attributeKey: 'powerSupplyWattage', label: 'Redundant Power Supply (PSU)', dataType: 'NUMBER', isRequired: true, unit: 'Watts', description: 'Titanium-rated dual PSU wattage' }
  ],
  'cat_srv_gpu': [
    { attributeKey: 'gpuCount', label: 'GPU Accelerator Count', dataType: 'NUMBER', isRequired: true, unit: 'GPUs', description: 'Number of enterprise SXM5/PCIe accelerators' },
    { attributeKey: 'interconnectType', label: 'GPU Interconnect Mesh', dataType: 'ENUM', isRequired: true, allowedValues: ['NVLink 4.0', 'Infinity Fabric', 'PCIe 5.0 x16'], description: 'High-speed GPU mesh fabric' },
    { attributeKey: 'gpuMemoryGb', label: 'Aggregate HBM3 Memory', dataType: 'NUMBER', isRequired: true, unit: 'GB', description: 'High Bandwidth Memory capacity' },
    { attributeKey: 'fp16TensorTflops', label: 'FP16 Tensor Compute Throughput', dataType: 'NUMBER', isRequired: true, unit: 'TFLOPS', description: 'Dense matrix multiplication performance' },
    { attributeKey: 'liquidCoolingReady', label: 'Direct-to-Chip Liquid Cooling', dataType: 'BOOLEAN', isRequired: true, description: 'CDU quick-disconnect loop compatibility' }
  ],
  'cat_san_allflash': [
    { attributeKey: 'rawCapacityTb', label: 'Raw All-Flash Capacity', dataType: 'NUMBER', isRequired: true, unit: 'TB', description: 'Unformatted TLC/QLC NVMe flash capacity' },
    { attributeKey: 'effectiveCapacityTb', label: 'Effective Capacity (5:1 Data Reduction)', dataType: 'NUMBER', isRequired: true, unit: 'TB', description: 'Usable capacity after deduplication and LZ4 compression' },
    { attributeKey: 'randomReadIops', label: '4KB Random Read IOPS', dataType: 'NUMBER', isRequired: true, unit: 'IOPS', description: 'Sub-millisecond latency sustained IOPS' },
    { attributeKey: 'hostInterfaces', label: 'Front-End Host Fabric', dataType: 'ENUM', isRequired: true, allowedValues: ['32G Fibre Channel', '100G NVMe-oF RoCEv2', '25GbE iSCSI'], description: 'SAN host protocol attachment' }
  ],
  'cat_net_switches_100g': [
    { attributeKey: 'portDensity', label: 'QSFP28 Port Count', dataType: 'NUMBER', isRequired: true, unit: 'ports', description: '100GbE physical cage density' },
    { attributeKey: 'switchingBandwidthTbps', label: 'Switching Fabric Bandwidth', dataType: 'NUMBER', isRequired: true, unit: 'Tbps', description: 'Full-duplex non-blocking ASIC bandwidth' },
    { attributeKey: 'forwardingRateMpps', label: 'Packet Forwarding Rate', dataType: 'NUMBER', isRequired: true, unit: 'Mpps', description: 'Line-rate L2/L3 packet throughput' },
    { attributeKey: 'supportedProtocols', label: 'Routing Protocols Supported', dataType: 'STRING', isRequired: true, description: 'BGP EVPN, VXLAN, RoCEv2, PFC, ECN' }
  ]
};

export class CategorySchemaResolver {
  public static getSchema(categoryId: string): CategoryAttributeField[] {
    return ENTERPRISE_CATEGORY_ATTRIBUTE_SCHEMAS[categoryId] || [];
  }
}
