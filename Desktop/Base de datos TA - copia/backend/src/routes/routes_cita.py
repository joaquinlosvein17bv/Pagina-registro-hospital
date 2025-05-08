import json

from fastapi import HTTPException
import mysql
from basededatos import get_db_connection
from fastapi import APIRouter
from models.model_cita import CitaIn
# --- Nuevo endpoint para crear cita leyendo el JSON ---
cita_router = APIRouter()
@cita_router.post("/citas/")
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
