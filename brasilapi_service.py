import httpx
from fastapi import HTTPException


async def buscar_cnpj(cnpj: str) -> dict:
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.get(url, timeout=10.0)
            resposta.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Não foi possível consultar a BrasilAPI")

    return resposta.json()

async def buscar_feriados(ano: int) -> list:
    url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.get(url, timeout=10.0)
            resposta.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Não foi possível consultar a BrasilAPI")

    return resposta.json()

async def buscar_cep(cep:str) -> dict:
    url = f"https://brasilapi.com.br/api/cep/v1/{cep}"

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.get(url, timeout=10.0)
            resposta.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Não foi possível consultar a BrasilAPI")

    return resposta.json()