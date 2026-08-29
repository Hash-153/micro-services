import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_pinnacle_modules():
    print("Generating comprehensive Quantum Pinnacle Modules...")

    # 1. API Gateway Path Regex Matcher & Trie Router
    write_file("services/api-gateway/src/router/path-trie-router.ts", """export interface TrieNode<T> {
  part: string;
  isWildcard: boolean;
  isParam: boolean;
  paramName?: string;
  handler?: T;
  children: Map<string, TrieNode<T>>;
}

export class PathTrieRouter<T> {
  private root: TrieNode<T> = {
    part: '',
    isWildcard: false,
    isParam: false,
    children: new Map()
  };

  public insert(pathPattern: string, handler: T): void {
    const segments = pathPattern.split('/').filter(Boolean);
    let current = this.root;

    for (const seg of segments) {
      const isParam = seg.startsWith(':');
      const isWildcard = seg === '*';
      const key = isParam ? ':param' : isWildcard ? '*' : seg;

      if (!current.children.has(key)) {
        current.children.set(key, {
          part: seg,
          isWildcard,
          isParam,
          paramName: isParam ? seg.substring(1) : undefined,
          children: new Map()
        });
      }
      current = current.children.get(key)!;
    }

    current.handler = handler;
  }

  public lookup(urlPath: string): { handler?: T; params: Record<string, string> } {
    const segments = urlPath.split('?')[0].split('/').filter(Boolean);
    const params: Record<string, string> = {};
    let current = this.root;

    for (const seg of segments) {
      if (current.children.has(seg)) {
        current = current.children.get(seg)!;
      } else if (current.children.has(':param')) {
        current = current.children.get(':param')!;
        if (current.paramName) {
          params[current.paramName] = seg;
        }
      } else if (current.children.has('*')) {
        current = current.children.get('*')!;
        break;
      } else {
        return { handler: undefined, params: {} };
      }
    }

    return { handler: current.handler, params };
  }
}
""")

    # 2. Database Distributed Pessimistic Lock Engine
    write_file("packages/core-database/src/pessimistic-lock-manager.ts", """import { Logger } from '@novacommerce/core-logger';

export class PessimisticLockManager {
  private logger: Logger;
  private lockedResources: Map<string, { lockHolderId: string; expiresAt: number }> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async acquireLock(resourceKey: string, lockHolderId: string, ttlMs: number = 5000): Promise<boolean> {
    const now = Date.now();
    const existing = this.lockedResources.get(resourceKey);

    if (existing && existing.expiresAt > now && existing.lockHolderId !== lockHolderId) {
      return false; // Resource locked by another transaction
    }

    this.lockedResources.set(resourceKey, {
      lockHolderId,
      expiresAt: now + ttlMs
    });

    this.logger.info(`Pessimistic lock acquired on '${resourceKey}' by holder '${lockHolderId}' (ttl=${ttlMs}ms)`);
    return true;
  }

  public async releaseLock(resourceKey: string, lockHolderId: string): Promise<boolean> {
    const existing = this.lockedResources.get(resourceKey);
    if (!existing || existing.lockHolderId !== lockHolderId) {
      return false;
    }

    this.lockedResources.delete(resourceKey);
    this.logger.info(`Pessimistic lock released on '${resourceKey}' by holder '${lockHolderId}'`);
    return true;
  }
}
""")

    print("Quantum pinnacle modules generated.")

if __name__ == "__main__":
    generate_quantum_pinnacle_modules()
