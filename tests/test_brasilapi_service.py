import httpx
import pytest
import respx

from brasilapi_service import buscar_cep, buscar_cnpj, buscar_feriados
from fastapi import HTTPException

@pytest.mark.asyncio
@respx.mock
async def test_buscar_cnpj_retorna_dados():
    url = "https://brasilapi.com.br/api/cnpj/v1/12345678000195"
    respx.get(url).mock(
        return_value=httpx.Response(200, json={"razao_social": "Empresa Teste"})
    )

    resultado = await buscar_cnpj("12345678000195")
    assert resultado == {"razao_social": "Empresa Teste"}


@pytest.mark.asyncio
@respx.mock
async def test_buscar_cnpj_levanta_erro_em_falha_http():
    url = "https://brasilapi.com.br/api/cnpj/v1/12345678000195"
    respx.get(url).mock(
        return_value=httpx.Response(500, json={"erro": "Erro interno do servidor"})
    )

    with pytest.raises(HTTPException):
        await buscar_cnpj("12345678000195")


@pytest.mark.asyncio
@respx.mock
async def test_buscar_feriados_retorna_dados():
    url = "https://brasilapi.com.br/api/feriados/v1/2024"
    respx.get(url).mock(
        return_value=httpx.Response(200, json=[{"date": "2024-01-01", "name": "Ano Novo"}])
    )

    resultado = await buscar_feriados(2024)
    assert resultado == [{"date": "2024-01-01", "name": "Ano Novo"}]


@pytest.mark.asyncio
@respx.mock
async def test_buscar_feriados_levanta_erro_em_falha_http():
    url = "https://brasilapi.com.br/api/feriados/v1/2024"
    respx.get(url).mock(
        return_value=httpx.Response(500, json={"erro": "Erro interno do servidor"})
    )

    with pytest.raises(HTTPException):
        await buscar_feriados(2024)


@pytest.mark.asyncio
@respx.mock
async def test_buscar_cep_retorna_dados():
    url = "https://brasilapi.com.br/api/cep/v1/01001000"
    respx.get(url).mock(
        return_value=httpx.Response(200, json={"state": "SP", "city": "São Paulo"})
    )

    resultado = await buscar_cep("01001000")
    assert resultado == {"state": "SP", "city": "São Paulo"}


@pytest.mark.asyncio
@respx.mock
async def test_buscar_cep_levanta_erro_em_falha_http():
    url = "https://brasilapi.com.br/api/cep/v1/01001000"
    respx.get(url).mock(
        return_value=httpx.Response(500, json={"erro": "Erro interno do servidor"})
    )

    with pytest.raises(HTTPException):
        await buscar_cep("01001000")