import pytest

from cache_repository import buscar_no_cache, salvar_no_cache


@pytest.mark.asyncio
async def test_salvar_e_buscar_no_cache(db_session):
    await salvar_no_cache(db_session, "chave_teste", {"valor": 42}, ttl_segundos=60)

    resultado = await buscar_no_cache(db_session, "chave_teste")

    assert resultado == {"valor": 42}

@pytest.mark.asyncio
async def test_buscar_chave_nao_salva(db_session):
    resultado = await buscar_no_cache(db_session, "chave_inexistente")

    assert resultado is None

@pytest.mark.asyncio
async def test_buscar_chave_expirada(db_session):
    await salvar_no_cache(db_session, "chave_expirada", {"valor": 42}, ttl_segundos=-1)

    resultado = await buscar_no_cache(db_session, "chave_expirada")

    assert resultado is None

@pytest.mark.asyncio
async def test_atualizar_chave_duplicada(db_session):
    await salvar_no_cache(db_session, "chave_duplicada", {"valor": 1}, ttl_segundos=60)
    await salvar_no_cache(db_session, "chave_duplicada", {"valor": 2}, ttl_segundos=60)

    resultado = await buscar_no_cache(db_session, "chave_duplicada")

    assert resultado == {"valor": 2}