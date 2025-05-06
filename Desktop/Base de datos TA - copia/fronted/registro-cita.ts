console.log("¡Módulo registro-cita cargado!");

// Otro nombre distinto para no chocar con el otro archivo.
const API_URL_CITA = "http://127.0.0.1:8000";

async function registrarCita(event: Event) {
  event.preventDefault();
  console.log("¡Formulario cita enviado!");

  // Ya no necesitas enviar paciente_id, el backend lo leerá del JSON.
  const fechaCita    = (document.getElementById("fecha-cita")   as HTMLInputElement).value;
  const especialidad = (document.getElementById("especialidad") as HTMLSelectElement).value;
  const profesional  = (document.getElementById("profesional")  as HTMLSelectElement).value;
  const motivo       = (document.getElementById("motivo")       as HTMLTextAreaElement).value;
  const ubicacion    = (document.getElementById("ubicacion")    as HTMLInputElement).value;

  const citaData = { fecha_cita: fechaCita, especialidad, profesional, motivo, ubicacion };

  try {
    const res = await fetch(`${API_URL_CITA}/citas/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(citaData),
    });
    if (!res.ok) throw new Error(`Error ${res.status} al crear cita`);

    const cita = await res.json();
    alert(`Cita registrada con éxito. ID: ${cita.id}`);
    window.location.href = "index.html";
  } catch (e: unknown) {
    alert(e instanceof Error ? e.message : "Error inesperado");
  }
}

document
  .getElementById("form-cita")!
  .addEventListener("submit", registrarCita);
