# Modelos Pydantic
from datetime import datetime
from pydantic import BaseModel


class Paciente(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str
    fecha_nacimiento: datetime
