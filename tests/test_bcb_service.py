import httpx
import pytest
import respx

from bcb_service import buscar_serie
from fastapi import HTTPException

@pytest.mark.asyncio
@respx.mock
async def test_buscar_serie_retorna_dados():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/5"
    respx.get(url).mock(
        return_value=httpx.Response(200, json=[{"data": "01/08/2026", "valor": "10.75"}])
    )

    resultado = await buscar_serie(codigo=11, ultimos_n=5)

    assert resultado == [{"data": "01/08/2026", "valor": "10.75"}]


@pytest.mark.asyncio
@respx.mock
async def test_buscar_serie_levanta_erro_em_falha_http():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/5"
    respx.get(url).mock(
        return_value=httpx.Response(500, json={"erro": "Erro interno do servidor"})
    )

    with pytest.raises(HTTPException):
        await buscar_serie(codigo=11, ultimos_n=5)


