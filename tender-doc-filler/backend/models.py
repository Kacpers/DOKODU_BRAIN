from __future__ import annotations
from enum import Enum
from pydantic import BaseModel


class AnalysisMode(str, Enum):
    RULE = "rule"
    AI = "ai"
    HYBRID = "hybrid"


class FieldSource(str, Enum):
    RULE = "rule"
    AI = "ai"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FieldResult(BaseModel):
    location_id: str
    location_type: str
    label: str
    original_value: str
    filled_value: str
    source: FieldSource
    confidence: Confidence


class AnalysisResponse(BaseModel):
    document_id: str
    filename: str
    mode: AnalysisMode
    fields: list[FieldResult]
    total_fields: int
    filled_fields: int


class CompanyProfile(BaseModel):
    nazwa_firmy: str = ""
    nip: str = ""
    regon: str = ""
    krs: str = ""
    adres: str = ""
    adres_korespondencyjny: str = ""
    email: str = ""
    telefon: str = ""
    osoba_kontaktowa: str = ""
    stanowisko: str = ""
    status_przedsiebiorcy: str = ""
    miejscowosc: str = ""


class ErrorResponse(BaseModel):
    error: str
    code: str
