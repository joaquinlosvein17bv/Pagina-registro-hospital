from datetime import datetime

from pydantic import BaseModel


class CitaIn(BaseModel):
    fecha_cita: datetime
    especialidad: str
    profesional: str
    motivo: str | None = None
    ubicacion: str | None = None


class PacienteID(BaseModel):
    id: int