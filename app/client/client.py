import httpx
from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class BaseExternalClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.timeout = timeout

    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None, 
        data: Optional[Dict[str, Any]] = None
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=data
                )
                # Lanza una excepción si el status es 4xx o 5xx
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                # Aquí traduces errores de la API externa a errores de FastAPI
                detail = f"Error en servicio externo: {e.response.text}"
                raise HTTPException(status_code=e.response.status_code, detail=detail)
            
            except httpx.RequestError as e:
                # Error de conexión, timeout, etc.
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Servicio externo no disponible: {str(e)}"
                )

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: Dict[str, Any]):
        return await self._request("POST", endpoint, data=data)