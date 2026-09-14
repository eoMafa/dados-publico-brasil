import json
from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from cache_model import CacheEntry


async def buscar_no_cache(db: AsyncSession, chave: str):
    resultado = await db.execute(select(CacheEntry).where(CacheEntry.chave == chave))
    entrada = resultado.scalar_one_or_none()

    if entrada is None:
        return None

    if entrada.expira_em < datetime.now(timezone.utc):
        return None

    return json.loads(entrada.valor)

async def salvar_no_cache(db: AsyncSession, chave: str, valor, ttl_segundos: int):
    expira_em = datetime.now(timezone.utc) + timedelta(seconds=ttl_segundos)
    valor_serializado = json.dumps(valor)

    stmt = insert(CacheEntry).values(
        chave=chave,
        valor=valor_serializado,
        expira_em=expira_em,
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["chave"],
        set_={"valor": valor_serializado, "expira_em": expira_em},
    )

    await db.execute(stmt)
    await db.commit()