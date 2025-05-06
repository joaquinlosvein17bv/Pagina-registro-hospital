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
console.log("¡Módulo registro-paciente cargado!");
// Le damos un nombre específico para que no choque con el otro archivo.
const API_URL_PACIENTE = "http://127.0.0.1:8000";
function registrarPaciente(event) {
    return __awaiter(this, void 0, void 0, function* () {
        event.preventDefault();
        console.log("¡Formulario paciente enviado!");
        const nombre = document.getElementById("nombre").value;
        const email = document.getElementById("email").value;
        const telefono = document.getElementById("telefono").value;
        const direccion = document.getElementById("direccion").value;
        const fn = document.getElementById("fecha-nacimiento").value;
        const pacienteData = { nombre, email, telefono, direccion, fecha_nacimiento: fn };
        try {
            const res = yield fetch(`${API_URL_PACIENTE}/pacientes/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(pacienteData),
            });
            if (!res.ok)
                throw new Error(`Error ${res.status} al crear paciente`);
            const paciente = yield res.json();
            alert(`Paciente registrado con éxito. ID: ${paciente.id}`);
            // Redirigir a cita
            window.location.href = "registro-cita.html";
        }
        catch (e) {
            alert(e instanceof Error ? e.message : "Error inesperado");
        }
    });
}
document
    .getElementById("registrar-paciente")
    .addEventListener("click", registrarPaciente);
