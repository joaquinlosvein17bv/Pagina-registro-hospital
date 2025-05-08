import json
from fastapi import FastAPI, HTTPException
from routes.routes_paciente import paciente_router
from routes.routes_cita import cita_router
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from fastapi.responses import FileResponse
from datetime import datetime
# Configuración DB (igual que antes)

app = FastAPI()
app.include_router(paciente_router)
app.include_router(cita_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


# Crear paciente (igual que antes)
