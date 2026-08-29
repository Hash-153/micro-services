import httpx
from typing import Dict, Any, Optional
from .exceptions import NovaCommerceException, AuthenticationError, NotFoundError, ValidationError, InsufficientStockError, SagaExecutionError

class ApiErrorHandler:
    @staticmethod
    def parse_and_raise(response: httpx.Response) -> None:
        try:
            body = response.json()
            err = body.get('error', {})
            msg = err.get('message', response.text)
            code = err.get('code', 'ERR_UNKNOWN')
            details = err.get('details')
        except Exception:
            msg = response.text
            code = 'ERR_HTTP'
            details = None

        status = response.status_code
        if status == 401:
            raise AuthenticationError(msg)
        elif status == 404:
            raise NotFoundError('Resource', response.url.path)
        elif status == 400:
            raise ValidationError(msg, details)
        elif status == 409 and code == 'ERR_INSUFFICIENT_STOCK':
            raise InsufficientStockError('SKU', 0, 0)
        else:
            raise NovaCommerceException(msg, status_code=status, error_code=code, details=details)
