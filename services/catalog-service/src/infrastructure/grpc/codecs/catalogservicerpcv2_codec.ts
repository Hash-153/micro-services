export interface CatalogServiceRpcV2Request {
  requestId: string;
  serviceCallerId: string;
  organizationId: string;
  payloadJson: string;
  timestamp: number;
}

export interface CatalogServiceRpcV2Response {
  requestId: string;
  isSuccess: boolean;
  statusCode: number;
  resultJson: string;
  errorMessage?: string;
  executionDurationMs: number;
}

export class CatalogServiceRpcV2Codec {
  public static encodeRequest(req: CatalogServiceRpcV2Request): Uint8Array {
    const jsonStr = JSON.stringify(req);
    return new TextEncoder().encode(jsonStr);
  }

  public static decodeRequest(buffer: Uint8Array): CatalogServiceRpcV2Request {
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }

  public static encodeResponse(res: CatalogServiceRpcV2Response): Uint8Array {
    const jsonStr = JSON.stringify(res);
    return new TextEncoder().encode(jsonStr);
  }

  public static decodeResponse(buffer: Uint8Array): CatalogServiceRpcV2Response {
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }
}
