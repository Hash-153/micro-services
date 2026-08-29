export interface InventoryServiceRpcV2Request {
  requestId: string;
  serviceCallerId: string;
  organizationId: string;
  payloadJson: string;
  timestamp: number;
}

export interface InventoryServiceRpcV2Response {
  requestId: string;
  isSuccess: boolean;
  statusCode: number;
  resultJson: string;
  errorMessage?: string;
  executionDurationMs: number;
}

export class InventoryServiceRpcV2Codec {
  public static encodeRequest(req: InventoryServiceRpcV2Request): Uint8Array {
    const jsonStr = JSON.stringify(req);
    return new TextEncoder().encode(jsonStr);
  }

  public static decodeRequest(buffer: Uint8Array): InventoryServiceRpcV2Request {
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }

  public static encodeResponse(res: InventoryServiceRpcV2Response): Uint8Array {
    const jsonStr = JSON.stringify(res);
    return new TextEncoder().encode(jsonStr);
  }

  public static decodeResponse(buffer: Uint8Array): InventoryServiceRpcV2Response {
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }
}
