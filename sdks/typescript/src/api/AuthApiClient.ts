import { RegisterUserDTO, LoginUserDTO, AuthTokensResponseDTO, ApiResponse } from '@novacommerce/core-types';

export class AuthApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async register(dto: RegisterUserDTO): Promise<AuthTokensResponseDTO> {
    const res = await fetch(`${this.baseUrl}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Registration failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<AuthTokensResponseDTO>;
    return json.data;
  }

  public async login(dto: LoginUserDTO): Promise<AuthTokensResponseDTO> {
    const res = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Login failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<AuthTokensResponseDTO>;
    return json.data;
  }

  public async getProfile(): Promise<any> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Fetch profile failed: ${res.statusText}`);
    const json = await res.json();
    return json.data;
  }
}
