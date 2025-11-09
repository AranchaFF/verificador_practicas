import streamlit as st
import pandas as pd
import os
import io
import zipfile
from datetime import datetime as dt
from procesar_datos import (
    extraer_fichajes, validar_fichajes, actualizar_sepe, 
    registrar_historial, leer_texto_de_fichaje, 
    backup_sepe_file, get_fichajes_alumno, 
    PYTESSERACT_AVAILABLE
)

st.set_page_config(
    page_title="Verificador de Prácticas SEPE",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Verificador de Prácticas — SEPE")
st.markdown("**Sistema automático de validación de asistencia y fichajes**")

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Configuración")
    
    umbral_porcentaje = st.slider("Umbral mínimo asistencia (%)", 50, 100, 75)
    umbral_empresa = st.slider("Coincidencia mínima empresa (%)", 50, 100, 70)
    mostrar_imagenes = st.checkbox("Mostrar fichajes en detalle", True)
    
    st.markdown("---")
    
    if PYTESSERACT_AVAILABLE:
        st.success("✅ OCR disponible")
    else:
        st.info("ℹ️ OCR no disponible (solo archivos .txt)")

# CARGA DE ARCHIVOS
st.header("📁 Carga de archivos")

col1, col2 = st.columns(2)

with col1:
    alumnos_file = st.file_uploader("📄 Excel de alumnos", type=["xlsx", "xls"])
    curso_nombre = st.text_input("📝 Nombre del curso", "Curso_prueba")

with col2:
    sepe_file = st.file_uploader("📊 Plantilla SEPE", type=["xlsx", "xls"])
    zip_file = st.file_uploader("📦 ZIP con fichajes", type=["zip"])

archivos_cargados = all([alumnos_file, sepe_file, zip_file])

if archivos_cargados:
    st.success("✅ Todos los archivos cargados")
else:
    st.info("ℹ️ Por favor, carga los tres archivos")

# PROCESAMIENTO
if archivos_cargados:
    # Crear carpetas
    for carpeta in ["data", "output", "temp/fichajes", "backups", "historial"]:
        os.makedirs(carpeta, exist_ok=True)
    
    # Guardar archivos
    alumnos_path = "data/alumnos.xlsx"
    sepe_path = "data/sepe_plantilla.xlsx"
    zip_path = "data/fichajes.zip"
    
    for path, data in [(alumnos_path, alumnos_file), (sepe_path, sepe_file), (zip_path, zip_file)]:
        with open(path, "wb") as f:
            f.write(data.getbuffer())
    
    # Vista previa
    st.header("👀 Vista previa")
    
    try:
        with st.spinner("Extrayendo fichajes..."):
            extraer_fichajes(zip_path, "temp/fichajes")
        
        df_alumnos = pd.read_excel(alumnos_path)
        df_sepe = pd.read_excel(sepe_path)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Alumnos", df_alumnos['ID'].nunique())
        with col2:
            st.metric("📚 Módulos", len(df_alumnos))
        with col3:
            fichajes_count = len([f for f in os.listdir("temp/fichajes") if os.path.isfile(os.path.join("temp/fichajes", f))])
            st.metric("📄 Fichajes", fichajes_count)
        
        with st.expander("📋 Ver datos de alumnos"):
            st.dataframe(df_alumnos, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.stop()
    
    st.markdown("---")
    
    if st.button("🚀 EJECUTAR VALIDACIÓN", type="primary", use_container_width=True):
        try:
            with st.spinner("🔄 Procesando..."):
                backup_path = backup_sepe_file(sepe_path)
                df_resultados = validar_fichajes(df_alumnos, "temp/fichajes", umbral_porcentaje, umbral_empresa)
                df_sepe_actual = actualizar_sepe(df_sepe, df_resultados)
                
                out_informe = "output/informe_validacion.xlsx"
                out_sepe = "output/sepe_actualizado.xlsx"
                
                df_resultados.to_excel(out_informe, index=False)
                df_sepe_actual.to_excel(out_sepe, index=False)
                
                hist_path = registrar_historial(curso_nombre, df_resultados)
            
            st.success("✅ ¡Validación completada!")
            
            # RESULTADOS
            st.header("📊 Resultados")
            
            total = len(df_resultados)
            cumplen_asist = (df_resultados['Cumple_75%'] == '✓').sum()
            cumplen_emp = (df_resultados['Coincide_empresa'] == '✓').sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", total)
            with col2:
                pct = round((cumplen_asist / total) * 100, 1) if total > 0 else 0
                st.metric("✅ Cumplen asistencia", f"{cumplen_asist} ({pct}%)")
            with col3:
                pct = round((cumplen_emp / total) * 100, 1) if total > 0 else 0
                st.metric("🏢 Empresa correcta", f"{cumplen_emp} ({pct}%)")
            
            st.dataframe(df_resultados, use_container_width=True, hide_index=True)
            
            # DESCARGAS
            st.header("📥 Descargas")
            
            col1, col2 = st.columns(2)
            with col1:
                with open(out_informe, "rb") as f:
                    st.download_button("📄 Descargar informe", f, "informe_validacion.xlsx")
            with col2:
                with open(out_sepe, "rb") as f:
                    st.download_button("📊 Descargar SEPE actualizado", f, "sepe_actualizado.xlsx")
            
            st.info(f"💾 Backup: `{os.path.basename(backup_path)}`")
            st.info(f"📁 Historial: `{os.path.basename(hist_path)}`")
            
            # VISOR POR ALUMNO
            st.markdown("---")
            st.header("👤 Visor por alumno")
            
            alumnos_unicos = df_resultados[['ID', 'Nombre']].drop_duplicates()
            opciones = [f"{row['ID']} - {row['Nombre']}" for _, row in alumnos_unicos.iterrows()]
            
            sel_alumno = st.selectbox("Seleccionar alumno", opciones)
            sel_id = sel_alumno.split(' - ')[0]
            
            df_alumno = df_resultados[df_resultados['ID'] == sel_id]
            
            st.subheader(f"Información de {sel_alumno}")
            st.dataframe(df_alumno, use_container_width=True, hide_index=True)
            
            if mostrar_imagenes:
                st.subheader("📄 Fichajes")
                archivos = get_fichajes_alumno("temp/fichajes", sel_id)
                
                if not archivos:
                    st.warning("⚠️ No se encontraron fichajes")
                else:
                    for i, archivo in enumerate(archivos, 1):
                        with st.expander(f"📄 Fichaje {i}: {os.path.basename(archivo)}", expanded=(i == 1)):
                            texto = leer_texto_de_fichaje(archivo)
                            if texto.strip():
                                st.text_area("Texto extraído", texto, height=200)
                            else:
                                st.warning("No se pudo extraer texto")
            
            if st.button("📦 Generar ZIP de evidencias", use_container_width=True):
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, "w") as zf:
                    df_alumno.to_excel("temp_alumno.xlsx", index=False)
                    zf.write("temp_alumno.xlsx", f"informe_{sel_id}.xlsx")
                    os.remove("temp_alumno.xlsx")
                    
                    for archivo in archivos:
                        zf.write(archivo, os.path.join("fichajes", os.path.basename(archivo)))
                
                buffer.seek(0)
                st.download_button("⬇️ Descargar ZIP", buffer, f"evidencias_{sel_id}.zip")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")