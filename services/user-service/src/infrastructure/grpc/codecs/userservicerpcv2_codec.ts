export interface UserServiceRpcV2Request {
  requestId: string;
  serviceCallerId: string;
  organizationId: string;
  payloadJson: string;
  timestamp: number;
}

export interface UserServiceRpcV2Response {
  requestId: string;
  isSuccess: boolean;
  statusCode: number;
  resultJson: string;
  errorMessage?: string;
  executionDurationMs: number;
}

export class UserServiceRpcV2Codec {
  public static encodeRequest(req: UserServiceRpcV2Request): Uint8Array {
    const jsonStr = JSON.stringify(req);
    return new TextEncoder().encode(jsonStr);
  }

  public static decodeRequest(buffer: Uint8Array): UserServiceRpcV2Request {
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }

  public static encodeResponse(res: UserServiceRpcV2Response): Uint8Array {
    const jsonStr = JSON.stringify(res);
    return new TextEncoder().encode(jsonStr);
  }

  public static decodeResponse(buffer: Uint8Array): UserServiceRpcV2Response {
    const jsonStr = new TextDecoder().decode(buffer);
    return JSON.parse(jsonStr);
  }
}
