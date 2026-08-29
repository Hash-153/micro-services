import { MockGrpcClientPool } from '../src/index.js';

describe('Core gRPC Suite', () => {
  it('should pool and return connected client instance', async () => {
    const mockFactory = (cfg: any) => ({
      host: cfg.host,
      port: cfg.port,
      ping: () => 'pong'
    });

    const pool = new MockGrpcClientPool({ host: 'localhost', port: 50051 }, mockFactory);
    const client = await pool.getClient();

    expect(client.host).toBe('localhost');
    expect(client.port).toBe(50051);
    expect(client.ping()).toBe('pong');
  });
});
