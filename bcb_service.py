import httpx
from fastapi import HTTPException


async def buscar_serie(codigo: int, ultimos_n: int) -> list:
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/{ultimos_n}"

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.get(url, params={"formato": "json"}, timeout=10.0)
            resposta.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Não foi possível consultar o Banco Central")

    return resposta.json()