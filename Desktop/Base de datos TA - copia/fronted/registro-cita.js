"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
console.log("¡Módulo registro-cita cargado!");
// Otro nombre distinto para no chocar con el otro archivo.
const API_URL_CITA = "http://127.0.0.1:8000";
function registrarCita(event) {
    return __awaiter(this, void 0, void 0, function* () {
        event.preventDefault();
        console.log("¡Formulario cita enviado!");
        // Ya no necesitas enviar paciente_id, el backend lo leerá del JSON.
        const fechaCita = document.getElementById("fecha-cita").value;
        const especialidad = document.getElementById("especialidad").value;
        const profesional = document.getElementById("profesional").value;
        const motivo = document.getElementById("motivo").value;
        const ubicacion = document.getElementById("ubicacion").value;
        const citaData = { fecha_cita: fechaCita, especialidad, profesional, motivo, ubicacion };
        try {
            const res = yield fetch(`${API_URL_CITA}/citas/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(citaData),
            });
            if (!res.ok)
                throw new Error(`Error ${res.status} al crear cita`);
            const cita = yield res.json();
            alert(`Cita registrada con éxito. ID: ${cita.id}`);
            window.location.href = "index.html";
        }
        catch (e) {
            alert(e instanceof Error ? e.message : "Error inesperado");
        }
    });
}
document
    .getElementById("form-cita")
    .addEventListener("submit", registrarCita);
