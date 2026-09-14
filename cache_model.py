from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CacheEntry(Base):
    __tablename__ = "cache_entries"

    chave: Mapped[str] = mapped_column(String(255), primary_key=True)
    valor: Mapped[str] = mapped_column(Text)
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True))