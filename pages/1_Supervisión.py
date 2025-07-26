
import streamlit as st
import pandas as pd
from datetime import datetime
from util.centros_loader import cargar_centros
from google.oauth2.service_account import Credentials
import gspread
import io

# Verificación de sesión
if "logueado" not in st.session_state or not st.session_state.logueado:
    st.warning("Debe iniciar sesión para acceder.")
    st.stop()

# Cargar centros
df = cargar_centros()

st.title("📋 Formulario de Supervisión CATSPAT")

# Selección de ubicación
paises = df["País"].unique()
pais = st.selectbox("País", paises)

departamentos = df[df["País"] == pais]["Departamento"].unique()
departamento = st.selectbox("Departamento", departamentos)

sitios = df[(df["País"] == pais) & (df["Departamento"] == departamento)]["Nombre del Sitio"].unique()
sitio = st.selectbox("Unidad de Salud", sitios)

st.markdown("---")

# Preguntas
st.subheader("📝 Preguntas de Supervisión")

preguntas = [
    "¿El sitio cuenta con personal capacitado?",
    "¿Se aplican correctamente los protocolos?",
    "¿Existe registro actualizado de usuarios?",
    "¿Se realiza supervisión interna periódica?",
    "¿Hay evidencia de mejora continua?"
]

opciones = {"Sí": 1, "Parcial": 0.5, "No": 0}
respuestas = []

for pregunta in preguntas:
    respuesta = st.radio(pregunta, list(opciones.keys()), key=pregunta)
    respuestas.append(opciones[respuesta])

# Observaciones
observaciones = st.text_area("Observaciones adicionales (opcional):")

# Cálculo de puntaje
total_puntos = sum(respuestas)
porcentaje = (total_puntos / len(preguntas)) * 100

if porcentaje >= 80:
    resultado = "Cumple ✅"
elif porcentaje >= 60:
    resultado = "Parcialmente cumple ⚠️"
else:
    resultado = "No cumple ❌"

st.markdown("---")
st.write(f"**Puntaje Total:** {total_puntos} / {len(preguntas)}")
st.write(f"**Porcentaje:** {porcentaje:.1f}%")
st.write(f"**Resultado:** {resultado}")

# Guardar en Google Sheets
if st.button("Guardar Supervisión"):
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"]).worksheet(st.secrets["google_sheets"]["sheet_name"])

    fila = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pais, departamento, sitio] + respuestas + [total_puntos, porcentaje, resultado, observaciones]
    sheet.append_row(fila)
    st.success("✅ Supervisión guardada exitosamente.")
