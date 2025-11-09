import os
import zipfile
import re
import shutil
from datetime import datetime as dt, timedelta
from collections import defaultdict
import pandas as pd
from rapidfuzz import fuzz

# OCR desactivado (solo archivos .txt)
PYTESSERACT_AVAILABLE = False


# -------------------------
# UTILIDADES
# -------------------------

def normalizar_texto(texto):
    """Normaliza texto para comparaciones."""
    return re.sub(r'\s+', ' ', texto.lower().strip())


def extraer_nombre_empresa(texto, max_lineas=5):
    """Extrae nombre de empresa de las primeras líneas del texto."""
    lineas = [l.strip() for l in texto.split('\n') if l.strip()][:max_lineas]
    
    # Buscar patrones comunes de empresa
    patrones_empresa = [
        r'empresa[:\s]+(.+)',
        r'centro[:\s]+(.+)',
        r'^([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+(?:S\.?L\.?|S\.?A\.?|SL|SA))',
    ]
    
    for linea in lineas:
        for patron in patrones_empresa:
            match = re.search(patron, linea, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    
    # Si no hay patrón, devolver primera línea no vacía
    return lineas[0] if lineas else "Desconocida"


# -------------------------
# EXTRACCIÓN Y LECTURA
# -------------------------

def extraer_fichajes(zip_path, dest_folder):
    """Extrae las imágenes o txt del zip de fichajes."""
    os.makedirs(dest_folder, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Filtrar archivos ocultos y del sistema
        archivos = [f for f in zf.namelist() 
                   if not f.startswith('__MACOSX') 
                   and not f.startswith('.')
                   and not f.endswith('/')]
        
        for archivo in archivos:
            zf.extract(archivo, dest_folder)
    
    return dest_folder


def leer_texto_de_fichaje(ruta):
    """Lee texto desde archivos .txt."""
    if not os.path.exists(ruta):
        return ""
    
    ext = os.path.splitext(ruta)[1].lower()
    texto = ""
    
    if ext == ".txt":
        try:
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()
        except Exception as e:
            print(f"Error leyendo {ruta}: {e}")
    
    return texto


def extraer_horas_trabajadas(texto):
    """
    Extrae horas trabajadas a partir del texto.
    Soporta múltiples formatos: HH:MM, HH.MM, rangos, etc.
    """
    if not texto:
        return 0
    
    # Patrones de entrada-salida
    patrones = [
        r'entrada[:\s]*(\d{1,2}[:.]\d{2}).*?salida[:\s]*(\d{1,2}[:.]\d{2})',
        r'(\d{1,2}[:.]\d{2})\s*[-–—]\s*(\d{1,2}[:.]\d{2})',
        r'de\s+(\d{1,2}[:.]\d{2})\s+a\s+(\d{1,2}[:.]\d{2})',
    ]
    
    for patron in patrones:
        matches = re.finditer(patron, texto, flags=re.IGNORECASE | re.DOTALL)
        total_horas = 0
        
        for match in matches:
            h1, h2 = match.groups()
            
            # Normalizar formato
            h1 = h1.replace('.', ':')
            h2 = h2.replace('.', ':')
            
            try:
                from datetime import datetime
                t1 = datetime.strptime(h1, "%H:%M")
                t2 = datetime.strptime(h2, "%H:%M")
                
                # Calcular diferencia
                diff = t2 - t1
                if diff.total_seconds() < 0:
                    diff += timedelta(days=1)
                
                horas = diff.total_seconds() / 3600
                
                # Validar rango razonable (entre 1 y 12 horas)
                if 1 <= horas <= 12:
                    total_horas += horas
                    
            except ValueError:
                continue
        
        if total_horas > 0:
            return round(total_horas, 2)
    
    # Patrón de total de horas explícito
    match_total = re.search(r'total[:\s]*(\d{1,2}(?:[:.]\d{1,2})?)\s*h', texto, re.IGNORECASE)
    if match_total:
        try:
            return float(match_total.group(1).replace(':', '.'))
        except ValueError:
            pass
    
    return 0


# -------------------------
# VALIDACIÓN PRINCIPAL
# -------------------------

def validar_fichajes(df_alumnos, fichajes_folder, umbral_porcentaje=75, umbral_empresa=70):
    """
    Valida los fichajes contra los datos de alumnos.
    Retorna DataFrame con resultados detallados.
    """
    if not os.path.exists(fichajes_folder):
        raise FileNotFoundError(f"No existe la carpeta: {fichajes_folder}")
    
    # Indexar fichajes por alumno
    fichajes_por_alumno = defaultdict(list)
    
    for filename in os.listdir(fichajes_folder):
        filepath = os.path.join(fichajes_folder, filename)
        if not os.path.isfile(filepath):
            continue
        
        # Extraer ID del nombre del archivo
        match_id = re.search(r'([A-Z]\d{3,})', filename, re.IGNORECASE)
        if match_id:
            alumno_id = match_id.group(1).upper()
            fichajes_por_alumno[alumno_id].append(filepath)
    
    resultados = []
    
    for _, row in df_alumnos.iterrows():
        alumno_id = str(row.get("ID", "")).strip().upper()
        nombre = str(row.get("Nombre", "")).strip()
        empresa_asig = str(row.get("Empresa_asignada", "")).strip()
        modulo = str(row.get("Módulo", "")).strip()
        horas_totales = float(row.get("Horas_totales", 0))
        
        # Buscar fichajes del alumno
        fichajes = fichajes_por_alumno.get(alumno_id, [])
        
        horas_real = 0
        empresas_detectadas = []
        num_fichajes = len(fichajes)
        observaciones = []
        
        # Procesar cada fichaje
        for fichaje_path in fichajes:
            texto = leer_texto_de_fichaje(fichaje_path)
            
            if not texto:
                observaciones.append(f"Fichaje vacío: {os.path.basename(fichaje_path)}")
                continue
            
            # Extraer horas
            horas = extraer_horas_trabajadas(texto)
            horas_real += horas
            
            # Extraer empresa
            empresa = extraer_nombre_empresa(texto)
            if empresa and empresa != "Desconocida":
                empresas_detectadas.append(empresa)
        
        # Empresa más común detectada
        if empresas_detectadas:
            empresa_detectada = max(set(empresas_detectadas), key=empresas_detectadas.count)
        else:
            empresa_detectada = "No detectada"
            observaciones.append("No se detectó empresa en ningún fichaje")
        
        # Validar empresa
        empresa_match = fuzz.partial_ratio(
            normalizar_texto(empresa_asig),
            normalizar_texto(empresa_detectada)
        )
        coincide_empresa = empresa_match >= umbral_empresa
        
        # Calcular porcentaje de asistencia
        pct_asistencia = round((horas_real / horas_totales) * 100, 2) if horas_totales > 0 else 0
        cumple_asistencia = pct_asistencia >= umbral_porcentaje
        
        # Observaciones adicionales
        if num_fichajes == 0:
            observaciones.append("⚠️ No se encontraron fichajes")
        elif horas_real == 0:
            observaciones.append("⚠️ No se detectaron horas en los fichajes")
        
        if not coincide_empresa and empresa_detectada != "No detectada":
            observaciones.append(f"⚠️ Empresa no coincide (similaridad: {empresa_match}%)")
        
        if horas_real > horas_totales * 1.2:
            observaciones.append("⚠️ Horas detectadas superan lo esperado en más del 20%")
        
        resultados.append({
            "ID": alumno_id,
            "Nombre": nombre,
            "Empresa_asignada": empresa_asig,
            "Empresa_detectada": empresa_detectada,
            "Coincide_empresa": "✓" if coincide_empresa else "✗",
            "Similaridad_empresa_%": empresa_match,
            "Módulo": modulo,
            "Horas_esperadas": horas_totales,
            "Horas_reales": round(horas_real, 2),
            "% asistencia": pct_asistencia,
            "Cumple_75%": "✓" if cumple_asistencia else "✗",
            "Num_fichajes": num_fichajes,
            "Observaciones": " | ".join(observaciones) if observaciones else "OK"
        })
    
    return pd.DataFrame(resultados)


# -------------------------
# ACTUALIZACIÓN SEPE
# -------------------------

def actualizar_sepe(df_sepe, df_resultados):
    """
    Actualiza el Excel SEPE con los % reales de asistencia.
    Crea columnas dinámicas por módulo si no existen.
    """
    df_actualizado = df_sepe.copy()
    
    # Normalizar nombres para matching
    df_actualizado['Nombre_normalizado'] = df_actualizado['Nombre'].apply(normalizar_texto)
    
    for _, row in df_resultados.iterrows():
        nombre_alumno = normalizar_texto(str(row['Nombre']))
        modulo = str(row['Módulo'])
        pct = row['% asistencia']
        
        # Buscar alumno en SEPE
        mask = df_actualizado['Nombre_normalizado'] == nombre_alumno
        
        if not mask.any():
            # Intentar matching fuzzy
            for idx, nombre_sepe in df_actualizado['Nombre_normalizado'].items():
                if fuzz.ratio(nombre_alumno, nombre_sepe) > 85:
                    mask = df_actualizado.index == idx
                    break
        
        if not mask.any():
            continue
        
        # Crear columna si no existe
        col_modulo = f"Modulo_{modulo}_%"
        if col_modulo not in df_actualizado.columns:
            df_actualizado[col_modulo] = None
        
        # Actualizar porcentaje
        df_actualizado.loc[mask, col_modulo] = pct
    
    # Eliminar columna auxiliar
    df_actualizado.drop(columns=['Nombre_normalizado'], inplace=True)
    
    return df_actualizado


# -------------------------
# GESTIÓN DE ARCHIVOS
# -------------------------

def backup_sepe_file(sepe_path, backup_dir="backups"):
    """Crea copia de seguridad del archivo SEPE."""
    if not os.path.exists(sepe_path):
        raise FileNotFoundError(f"No se encontró el archivo SEPE: {sepe_path}")
    
    os.makedirs(backup_dir, exist_ok=True)
    
    base = os.path.basename(sepe_path)
    nombre, ext = os.path.splitext(base)
    ts = dt.now().strftime("%Y%m%d_%H%M%S")
    
    dest = os.path.join(backup_dir, f"{nombre}_backup_{ts}{ext}")
    shutil.copy2(sepe_path, dest)
    
    return dest


def registrar_historial(nombre_curso, df_result, historial_dir="historial"):
    """Guarda informe de validación en carpeta historial."""
    os.makedirs(historial_dir, exist_ok=True)
    
    # Limpiar nombre del curso para nombre de archivo
    nombre_limpio = re.sub(r'[^\w\s-]', '', nombre_curso).strip().replace(' ', '_')
    ts = dt.now().strftime("%Y%m%d_%H%M%S")
    
    filename = f"{nombre_limpio}_{ts}.xlsx"
    path = os.path.join(historial_dir, filename)
    
    df_result.to_excel(path, index=False)
    
    return path


def get_fichajes_alumno(fichajes_folder, id_alumno):
    """Obtiene lista de fichajes de un alumno específico."""
    fichajes = []
    
    if not os.path.exists(fichajes_folder):
        return fichajes
    
    id_normalizado = str(id_alumno).strip().upper()
    
    for filename in os.listdir(fichajes_folder):
        filepath = os.path.join(fichajes_folder, filename)
        
        if not os.path.isfile(filepath):
            continue
        
        # Buscar ID en el nombre del archivo
        if id_normalizado in filename.upper():
            fichajes.append(filepath)
    
    return sorted(fichajes)