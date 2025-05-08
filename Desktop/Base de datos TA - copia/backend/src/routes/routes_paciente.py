import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import mysql
from basededatos import get_db_connection
from models.model_paciente import Paciente
from models.model_cita import PacienteID
# Crear paciente (igual que antes)
paciente_router = APIRouter()
@paciente_router.post("/pacientes/")
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
@paciente_router.post("/guardar_id/")
async def guardar_id(payload: PacienteID):
    # Ahora FastAPI espera { "id": 123 }
    try:
        with open("paciente_id.json", "w") as f:
            json.dump(payload.dict(), f)
        return {"message": "ID guardado"}
    except Exception as e:
        raise HTTPException(500, f"Error al guardar ID: {e}")

# Servir el JSON (igual que antes)
@paciente_router.get("/paciente_id.json")
async def leer_id():
    try:
        return FileResponse("paciente_id.json", media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(404, "ID no encontrado")
