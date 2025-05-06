import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from fastapi.responses import FileResponse
from datetime import datetime
# Configuración DB (igual que antes)
config = {
    "host": "127.0.0.1",
    "port": "3306",
    "database": "clinica_bienestar",
    "user": "root",
    "password": "Quintanasalas17."
}
def get_db_connection():
    return mysql.connector.connect(**config)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Modelos Pydantic
class Paciente(BaseModel):
    nombre: str
    email: str
    telefono: str
    direccion: str
    fecha_nacimiento: datetime

class CitaIn(BaseModel):
    fecha_cita: datetime
    especialidad: str
    profesional: str
    motivo: str | None = None
    ubicacion: str | None = None

class PacienteID(BaseModel):
    id: int
# Crear paciente (igual que antes)
@app.post("/pacientes/")
async def crear_paciente(p: Paciente):
    try:
        # 1) Insertamos en la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pacientes (nombre, email, telefono, direccion, fecha_nacimiento) "
            "VALUES (%s, %s, %s, %s, %s)",
            (p.nombre, p.email, p.telefono, p.direccion, p.fecha_nacimiento)
        )
        conn.commit()

        # 2) Obtenemos el nuevo ID
        pid = cur.lastrowid
        cur.close()
        conn.close()

        # 3) Escribimos el ID en paciente_id.json
        try:
            with open("paciente_id.json", "w") as f:
                json.dump({"id": pid}, f)
        except Exception as e:
            # Si falla escribir el JSON, lanzamos 500 para que lo veas
            raise HTTPException(500, f"No se pudo actualizar paciente_id.json: {e}")

        # 4) Devolvemos al cliente los datos + id
        return {**p.dict(), "id": pid}

    except mysql.connector.Error as e:
        raise HTTPException(500, f"DB error: {e}")

# Guardar ID en JSON (igual que antes)
@app.post("/guardar_id/")
async def guardar_id(payload: PacienteID):
    # Ahora FastAPI espera { "id": 123 }
    try:
        with open("paciente_id.json", "w") as f:
            json.dump(payload.dict(), f)
        return {"message": "ID guardado"}
    except Exception as e:
        raise HTTPException(500, f"Error al guardar ID: {e}")

# Servir el JSON (igual que antes)
@app.get("/paciente_id.json")
async def leer_id():
    try:
        return FileResponse("paciente_id.json", media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(404, "ID no encontrado")

# --- Nuevo endpoint para crear cita leyendo el JSON ---
@app.post("/citas/")
async def crear_cita(c: CitaIn):
    # 1. Leer paciente_id desde el JSON
    try:
        with open("paciente_id.json") as f:
            data = json.load(f)
            paciente_id = data.get("id")
        if paciente_id is None:
            raise HTTPException(400, "ID de paciente no encontrado en JSON")
    except FileNotFoundError:
        raise HTTPException(404, "archivo paciente_id.json no existe")
    except json.JSONDecodeError:
        raise HTTPException(500, "JSON inválido en paciente_id.json")

    # 2. Insertar la cita usando ese paciente_id
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO citas (paciente_id, fecha_cita, especialidad, profesional, motivo, ubicacion) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (paciente_id, c.fecha_cita, c.especialidad, c.profesional, c.motivo, c.ubicacion)
        )
        conn.commit()
        cid = cur.lastrowid
        cur.close()
        conn.close()
        return {**c.dict(), "id": cid, "paciente_id": paciente_id}
    except mysql.connector.Error as e:
        raise HTTPException(500, f"DB error: {e}")
