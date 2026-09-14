from fastapi import FastAPI, HTTPException, Depends
from bcb_service import buscar_serie
from brasilapi_service import buscar_cnpj, buscar_feriados, buscar_cep
from models import Empresa, Endereco, PontoIndicador, Feriado
from contextlib import asynccontextmanager
from database import engine, Base, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from cache_repository import buscar_no_cache, salvar_no_cache
from fastapi.middleware.cors import CORSMiddleware

import cache_model 

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}

@app.get("/selic", response_model=list[PontoIndicador])
async def obter_selic(ultimos_n: int = 5, db: AsyncSession = Depends(get_db)):
    chave_cache = f"selic_{ultimos_n}"

    dados_em_cache = await buscar_no_cache(db, chave_cache)
    if dados_em_cache is not None:
        return dados_em_cache

    dados = await buscar_serie(codigo=11, ultimos_n=ultimos_n)
    await salvar_no_cache(db, chave_cache, dados, ttl_segundos=3600)

    return dados

@app.get("/ipca", response_model=list[PontoIndicador])
async def obter_ipca(ultimos_n: int = 5, db: AsyncSession = Depends(get_db)):
    chave_cache = f"ipca_{ultimos_n}"

    dados_em_cache = await buscar_no_cache(db, chave_cache)
    if dados_em_cache is not None:
        return dados_em_cache

    dados = await buscar_serie(codigo=433, ultimos_n=ultimos_n)
    await salvar_no_cache(db, chave_cache, dados, ttl_segundos=3600)

    return dados

@app.get("/dolar", response_model=list[PontoIndicador])
async def obter_dolar(ultimos_n: int = 5, db: AsyncSession = Depends(get_db)):
    chave_cache = f"dolar_{ultimos_n}"

    dados_em_cache = await buscar_no_cache(db, chave_cache)
    if dados_em_cache is not None:
        return dados_em_cache

    dados = await buscar_serie(codigo=1, ultimos_n=ultimos_n)
    await salvar_no_cache(db, chave_cache, dados, ttl_segundos=3600)

    return dados

@app.get("/cnpj/{cnpj}", response_model=Empresa)
async def obter_cnpj(cnpj: str, db: AsyncSession = Depends(get_db)):
    if not cnpj.isdigit() or len(cnpj) != 14:
        raise HTTPException(status_code=422, detail="CNPJ deve conter exatamente 14 dígitos numéricos, sem pontuação")

    chave_cache = f"cnpj_{cnpj}"
    dados_em_cache = await buscar_no_cache(db, chave_cache)
    if dados_em_cache is not None:
        return dados_em_cache
  
    dados = await buscar_cnpj(cnpj)
    
    resultado = {
        "razao_social": dados.get("razao_social"),
        "nome_fantasia": dados.get("nome_fantasia"),
        "situacao_cadastral": dados.get("descricao_situacao_cadastral"),
        "municipio": dados.get("municipio"),
        "uf": dados.get("uf"),
        "atividade_principal": dados.get("cnae_fiscal_descricao"),
        "codigo_atividade_principal": dados.get("cnae_fiscal"),
    }

    await salvar_no_cache(db, chave_cache, resultado, ttl_segundos=604800)

    return resultado

@app.get("/feriados/{ano}", response_model=list[Feriado])
async def obter_feriados(ano: int, db: AsyncSession = Depends(get_db)):
    chave_cache = f"feriados_{ano}"
    dados_em_cache  = await buscar_no_cache(db, chave_cache)
    if dados_em_cache is not None:
        return dados_em_cache

    dados = await buscar_feriados(ano)
    await salvar_no_cache(db, chave_cache, dados, ttl_segundos=604800)

    return dados

@app.get("/cep/{cep}", response_model=Endereco)
async def obter_cep(cep: str, db: AsyncSession = Depends(get_db)):
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        raise HTTPException(status_code=422, detail="CEP deve conter exatamente 8 dígitos numéricos")

    chave_cache = f"cep_{cep}"
    dados_em_cache = await buscar_no_cache(db, chave_cache)
    if dados_em_cache is not None:
        return dados_em_cache
    
    dados = await buscar_cep(cep_limpo)

    resultado = {
        "cep": cep_limpo,
        "state": dados.get("state"),
        "city": dados.get("city"),
        "neighborhood": dados.get("neighborhood"),
        "street": dados.get("street"),
        "ibge_cidade": dados.get("ibge", {}).get("city"),
        "ibge_uf": dados.get("ibge", {}).get("state"),
    }

    await salvar_no_cache(db, chave_cache, resultado, ttl_segundos=604800)

    return resultado