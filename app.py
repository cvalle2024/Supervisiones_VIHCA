
import streamlit as st

# Página de inicio con login simple
st.set_page_config(page_title="Sistema de Supervisión", layout="centered")

if "logueado" not in st.session_state:
    st.session_state.logueado = False

if not st.session_state.logueado:
    st.title("🔐 Iniciar sesión")
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if usuario == "admin" and contraseña == "admin":
            st.session_state.logueado = True
            st.rerun()
        else:
            st.error("Credenciales inválidas")
else:
    st.success("✅ Sesión iniciada correctamente.")
    st.switch_page("pages/1_Supervisión.py")
