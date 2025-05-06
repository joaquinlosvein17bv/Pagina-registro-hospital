console.log("¡Módulo registro-paciente cargado!");

// Le damos un nombre específico para que no choque con el otro archivo.
const API_URL_PACIENTE = "http://127.0.0.1:8000";

async function registrarPaciente(event: Event) {
  event.preventDefault();
  console.log("¡Formulario paciente enviado!");

  const nombre    = (document.getElementById("nombre")           as HTMLInputElement).value;
  const email     = (document.getElementById("email")            as HTMLInputElement).value;
  const telefono  = (document.getElementById("telefono")         as HTMLInputElement).value;
  const direccion = (document.getElementById("direccion")        as HTMLInputElement).value;
  const fn        = (document.getElementById("fecha-nacimiento") as HTMLInputElement).value;

  const pacienteData = { nombre, email, telefono, direccion, fecha_nacimiento: fn };

  try {
    const res = await fetch(`${API_URL_PACIENTE}/pacientes/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(pacienteData),
    });
    if (!res.ok) throw new Error(`Error ${res.status} al crear paciente`);

    const paciente = await res.json();
    alert(`Paciente registrado con éxito. ID: ${paciente.id}`);

    // Redirigir a cita
    window.location.href = "registro-cita.html";
  } catch (e: unknown) {
    alert(e instanceof Error ? e.message : "Error inesperado");
  }
}

document
  .getElementById("registrar-paciente")!
  .addEventListener("click", registrarPaciente);
