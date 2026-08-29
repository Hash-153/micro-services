export interface TrieNode<T> {
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
