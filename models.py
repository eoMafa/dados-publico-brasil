from pydantic import BaseModel


class Empresa(BaseModel):
    razao_social: str | None = None
    nome_fantasia: str | None = None
    situacao_cadastral: str | None = None
    municipio: str | None = None
    uf: str | None = None
    atividade_principal: str | None = None
    codigo_atividade_principal: int | None = None

class Endereco(BaseModel):
    cep: str
    state: str
    city: str
    neighborhood: str | None = None
    street: str | None = None
    ibge_cidade: str | None = None
    ibge_uf: str | None = None

class PontoIndicador(BaseModel):
    data: str
    valor: float

class Feriado(BaseModel):
    date: str
    name: str
    type: str
    weekday: str