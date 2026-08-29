from typing import Dict, Any, List, Optional
from urllib.parse import urlencode

class ApiQueryBuilder:
    def __init__(self):
        self._params: Dict[str, Any] = {}

    def page(self, page_number: int) -> 'ApiQueryBuilder':
        self._params['page'] = max(1, page_number)
        return self

    def limit(self, limit_count: int) -> 'ApiQueryBuilder':
        self._params['limit'] = min(100, max(1, limit_count))
        return self

    def sort_by(self, field: str, direction: str = 'asc') -> 'ApiQueryBuilder':
        self._params['sortBy'] = field
        self._params['sortOrder'] = 'asc' if direction.lower() == 'asc' else 'desc'
        return self

    def filter(self, field: str, value: Any) -> 'ApiQueryBuilder':
        if value is not None:
            self._params[field] = value
        return self

    def filter_in(self, field: str, values: List[Any]) -> 'ApiQueryBuilder':
        if values:
            self._params[field] = ','.join(str(v) for v in values)
        return self

    def build(self) -> Dict[str, Any]:
        return {k: v for k, v in self._params.items() if v is not None}

    def to_query_string(self) -> str:
        params = self.build()
        return f"?{urlencode(params)}" if params else ""
