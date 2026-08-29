import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_starlight_modules():
    print("Generating comprehensive Quantum Starlight Modules...")

    # 1. API Gateway Distributed Rate Limit Leaky Bucket Token Refiller
    write_file("services/api-gateway/src/middleware/leaky-bucket-limiter.ts", """export class LeakyBucketLimiter {
  private capacity: number;
  private leakRatePerSecond: number;
  private waterLevel: number = 0;
  private lastLeakTimestamp: number = Date.now();

  constructor(capacity: number = 100, leakRatePerSecond: number = 10) {
    this.capacity = capacity;
    this.leakRatePerSecond = leakRatePerSecond;
  }

  public allowRequest(cost: number = 1): boolean {
    this.leak();
    if (this.waterLevel + cost <= this.capacity) {
      this.waterLevel += cost;
      return true;
    }
    return false;
  }

  private leak(): void {
    const now = Date.now();
    const elapsedSeconds = (now - this.lastLeakTimestamp) / 1000;
    const leaked = elapsedSeconds * this.leakRatePerSecond;

    if (leaked > 0) {
      this.waterLevel = Math.max(0, this.waterLevel - leaked);
      this.lastLeakTimestamp = now;
    }
  }
}
""")

    # 2. Database Replica Weighted Round Robin Dispatcher
    write_file("packages/core-database/src/replica-weighted-dispatcher.ts", """export interface ReadReplicaNode {
  host: string;
  port: number;
  weight: number;
  currentActiveConnections: number;
  isHealthy: boolean;
}

export class ReplicaWeightedDispatcher {
  private replicas: ReadReplicaNode[];
  private currentIndex: number = 0;

  constructor(replicas: ReadReplicaNode[]) {
    this.replicas = replicas;
  }

  public getNextHealthyReplica(): ReadReplicaNode | null {
    const healthy = this.replicas.filter(r => r.isHealthy);
    if (healthy.length === 0) return null;

    // Weighted least connections
    return [...healthy].sort((a, b) => {
      const loadA = a.currentActiveConnections / a.weight;
      const loadB = b.currentActiveConnections / b.weight;
      return loadA - loadB;
    })[0];
  }
}
""")

    print("Quantum starlight modules generated.")

if __name__ == "__main__":
    generate_quantum_starlight_modules()
