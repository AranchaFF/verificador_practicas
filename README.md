# 📋 Verificador de Prácticas SEPE — SmartMind

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.39%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

**Sistema automatizado de validación de horas de prácticas para centros educativos**

[Características](#-características-principales) • [Instalación](#-instalación) • [Uso](#-uso) • [Documentación](#-documentación)

</div>

---

## 📖 Descripción

**Verificador de Prácticas SEPE** es una aplicación web desarrollada en Python + Streamlit que automatiza completamente el proceso de verificación de las horas de prácticas de los alumnos en empresas colaboradoras.

El sistema permite:
- ✅ Calcular automáticamente el **porcentaje de asistencia por módulo**
- ✅ Verificar si cada alumno supera el **75% obligatorio** del SEPE
- ✅ Generar informes compatibles con la **plantilla oficial del SEPE**
- ✅ Detectar automáticamente empresas y horas trabajadas desde fichajes
- ✅ Crear backups automáticos y mantener historial de validaciones

---

## 🎯 Características principales

### 🔍 Análisis inteligente de fichajes
- Extracción automática de horas desde archivos de texto
- Soporte para múltiples formatos horarios (HH:MM, HH.MM, rangos)
- Detección automática del nombre de empresa
- Validación de coincidencia empresa asignada vs. detectada

### 📊 Gestión de datos
- Carga masiva de fichajes mediante archivos ZIP
- Integración directa con Excel (alumnos y plantilla SEPE)
- Cálculo automático de porcentajes de asistencia
- Actualización inteligente de la plantilla SEPE

### 🛡️ Seguridad y trazabilidad
- Backups automáticos antes de cada actualización
- Historial completo de validaciones con timestamp
- Exportación de evidencias por alumno en formato ZIP
- Sistema de observaciones y alertas automáticas

### 🎨 Interfaz intuitiva
- Dashboard interactivo con métricas en tiempo real
- Visor detallado alumno por alumno
- Visualización de fichajes y textos extraídos
- Configuración personalizable de umbrales

---

## 💻 Requisitos del sistema

### Software necesario

| Componente | Versión mínima | Descarga |
|------------|----------------|----------|
| 🐍 Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| 💻 VS Code | Latest | [code.visualstudio.com](https://code.visualstudio.com/) |
| 🧩 Git | 2.0+ | [git-scm.com](https://git-scm.com/) |

### Dependencias Python

```txt
streamlit>=1.39.0
pandas>=2.2.0
openpyxl>=3.1.0
rapidfuzz>=3.6.0
python-dateutil>=2.8.0
```

> **Nota:** Para OCR de imágenes (opcional): `pytesseract`, `opencv-python`, `Pillow`

---

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/AranchaFF/verificador_practicas.git
cd verificador_practicas
```

### 2️⃣ Crear entorno virtual (recomendado)

**Windows:**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar entorno
.\.venv\Scripts\Activate
```

**Linux/macOS:**
```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno
source .venv/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias básicas
pip install streamlit pandas openpyxl rapidfuzz python-dateutil

# O instalar desde requirements.txt
pip install -r requirements.txt
```

### 4️⃣ Verificar instalación

```bash
python -c "import streamlit, pandas, openpyxl, rapidfuzz; print('✅ Instalación correcta')"
```

---

## 📂 Estructura del proyecto

```
verificador_practicas/
│
├── 📄 app.py                    # Aplicación principal Streamlit
├── 📄 procesar_datos.py         # Lógica de procesamiento y validación
├── 📄 requirements.txt          # Dependencias del proyecto
├── 📄 README.md                 # Documentación (este archivo)
│
├── 📁 data/                     # Archivos de entrada (autogenerado)
│   ├── alumnos.xlsx            # Datos de alumnos y módulos
│   ├── sepe_plantilla.xlsx     # Plantilla oficial SEPE
│   └── fichajes.zip            # Fichajes comprimidos
│
├── 📁 output/                   # Resultados generados (autogenerado)
│   ├── informe_validacion.xlsx # Informe completo de validación
│   └── sepe_actualizado.xlsx   # Plantilla SEPE actualizada
│
├── 📁 backups/                  # Copias de seguridad (autogenerado)
├── 📁 historial/                # Histórico de validaciones (autogenerado)
└── 📁 temp/fichajes/            # Fichajes extraídos (temporal)
```

---

## 🎮 Uso

### Iniciar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Flujo de trabajo

#### 1️⃣ **Preparar los archivos de entrada**

**`alumnos.xlsx`** - Debe contener estas columnas:

| ID | Nombre | Empresa_asignada | Módulo | Horas_totales |
|----|--------|------------------|--------|---------------|
| A001 | Ana Pérez | TechData SL | M1 | 100 |
| A001 | Ana Pérez | TechData SL | M2 | 80 |
| A002 | Luis García | Informática Norte SA | M1 | 120 |

**`sepe_plantilla.xlsx`** - Plantilla oficial del SEPE:

| Nombre | DNI | Curso | Modulo_M1_% | Modulo_M2_% |
|--------|-----|-------|-------------|-------------|
| Ana Pérez | 12345678A | Ciberseguridad | | |
| Luis García | 87654321B | Ciberseguridad | | |

**`fichajes.zip`** - Archivos de texto nombrados como:
- `A001_fichaje_01.txt`
- `A001_fichaje_M2_01.txt`
- `A002_fichaje_01.txt`

#### 2️⃣ **Cargar archivos en la aplicación**

1. Sube los tres archivos desde la interfaz web
2. Ajusta los umbrales si es necesario:
   - **Umbral de asistencia:** 75% (mínimo SEPE)
   - **Coincidencia empresa:** 70% (matching fuzzy)

#### 3️⃣ **Ejecutar validación**

1. Haz clic en **"🚀 EJECUTAR VALIDACIÓN"**
2. El sistema procesará automáticamente:
   - ✅ Extracción de fichajes del ZIP
   - ✅ Lectura y análisis de cada fichaje
   - ✅ Cálculo de horas trabajadas
   - ✅ Detección de empresas
   - ✅ Cálculo de porcentajes de asistencia
   - ✅ Actualización de la plantilla SEPE

#### 4️⃣ **Revisar resultados**

Verás un dashboard con:
- 📊 **Métricas generales:** Total alumnos, % que cumplen, alertas
- 📋 **Tabla completa:** Todos los resultados detallados
- 👤 **Visor por alumno:** Detalles individuales con fichajes
- 📄 **Observaciones:** Alertas automáticas de anomalías

#### 5️⃣ **Descargar informes**

- 📥 **Informe de validación:** Resultados completos en Excel
- 📥 **SEPE actualizado:** Plantilla oficial con porcentajes
- 📦 **ZIP de evidencias:** Por alumno (opcional)

---

## 📝 Formato de fichajes

### Ejemplo de fichaje en texto plano

```txt
Empresa: TechData SL
Fecha: 15/01/2025
Módulo: M1
Entrada: 09:00
Salida: 14:00
Observaciones: Jornada completa
```

### Formatos soportados

El sistema detecta automáticamente múltiples formatos:

```txt
# Formato 1: Entrada/Salida explícito
Entrada: 09:00
Salida: 13:00

# Formato 2: Rango con guión
09:00 - 17:00

# Formato 3: De...a
De 08:30 a 14:30

# Formato 4: Total explícito
Total: 6 horas
```

---

## 🧪 Datos de prueba

El repositorio incluye archivos de ejemplo en `/ejemplos/`:

```bash
# Copiar archivos de prueba
cp ejemplos/alumnos.xlsx data/
cp ejemplos/sepe_plantilla.xlsx data/
cp ejemplos/fichajes.zip data/
```

### Resultados esperados con datos de prueba

| Alumno | Módulo | Horas | % Asist. | Cumple | Empresa |
|--------|--------|-------|----------|--------|---------|
| Ana Pérez | M1 | 12h | 12% | ❌ | ✅ |
| Ana Pérez | M2 | 4h | 5% | ❌ | ✅ |
| Luis García | M1 | 15h | 12.5% | ❌ | ✅ |
| María López | M1 | 0h | 0% | ❌ | ⚠️ Sin fichajes |

---

## ⚙️ Configuración avanzada

### Umbrales personalizables

Desde el sidebar de la aplicación puedes ajustar:

- **Umbral mínimo de asistencia (%)**: Por defecto 75% (SEPE)
- **Coincidencia mínima empresa (%)**: Por defecto 70% (fuzzy matching)
- **Mostrar fichajes en detalle**: Activar/desactivar vista previa

### Variables de entorno (opcional)

```bash
# Activar modo debug
export STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true

# Cambiar puerto
export STREAMLIT_SERVER_PORT=8080
```

---

## 🛠️ Características técnicas

### Algoritmos implementados

- **Fuzzy matching** con RapidFuzz para detección de empresas
- **Expresiones regulares** para extracción de horarios
- **Normalización de texto** para comparaciones robustas
- **Validación de rangos** horarios (1-12h por fichaje)

### Validaciones automáticas

- ✅ Detección de fichajes vacíos o corruptos
- ✅ Alertas de horas excesivas (>120% esperado)
- ✅ Advertencias de empresas no coincidentes
- ✅ Control de alumnos sin fichajes

### Seguridad

- 🔒 Backups automáticos con timestamp
- 🔒 Historial inmutable de validaciones
- 🔒 No modificación de archivos originales
- 🔒 Validación de integridad de datos

---

## 📊 Casos de uso

### ✅ Centros educativos
- Validación masiva de prácticas FCT
- Generación de informes para auditorías SEPE
- Control de asistencia en empresas colaboradoras

### ✅ Departamentos de orientación
- Seguimiento individual de alumnos
- Detección temprana de incumplimientos
- Gestión de evidencias documentales

### ✅ Coordinadores de FP
- Supervisión de múltiples módulos y cursos
- Exportación de datos para memorias anuales
- Análisis de tasas de cumplimiento

---

## 🐛 Solución de problemas

### Error: "Import 'streamlit' could not be resolved"

**Causa:** VS Code no detecta el intérprete correcto

**Solución:**
1. Presiona `Ctrl + Shift + P`
2. Busca: `Python: Select Interpreter`
3. Selecciona el Python donde instalaste las librerías

### Error: "Module not found: pandas"

**Causa:** Dependencias no instaladas

**Solución:**
```bash
pip install -r requirements.txt
```

### Error al compilar numpy/pandas

**Causa:** Python 3.14 muy reciente, faltan compiladores

**Solución:**
```bash
# Instalar versión estable de Python 3.11
# O instalar Microsoft C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### La app no se abre en el navegador

**Causa:** Firewall o puerto ocupado

**Solución:**
```bash
# Usar puerto diferente
streamlit run app.py --server.port 8080

# O abrir manualmente: http://localhost:8501
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

## 🗺️ Roadmap

### Versión 2.0 (Próximamente)

- [ ] 🖼️ Soporte para OCR de imágenes (JPG, PNG, PDF)
- [ ] 📧 Notificaciones automáticas por email
- [ ] 📈 Gráficos interactivos de asistencia
- [ ] 🗄️ Base de datos SQLite para histórico
- [ ] 🔐 Sistema de autenticación multiusuario
- [ ] 📱 Diseño responsive para móviles
- [ ] 🌍 Soporte multiidioma (ES/EN)
- [ ] 📄 Exportación de informes en PDF

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 - Arancha Fernández

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y archivos de documentación asociados (el "Software"), para usar
el Software sin restricciones, **siempre que se incluya la atribución a Arancha Fernández** como autora original del proyecto.

El software se proporciona "tal cual", sin garantía de ningún tipo, expresa o implícita.
```

---

## 👥 Autores

**Arancha Fernández** - [GitHub](https://github.com/AranchaFF)

---

## 🙏 Agradecimientos

- Equipo de SmartMind por el apoyo en el desarrollo
- Comunidad de Streamlit por la excelente documentación
- SEPE por los estándares de validación de prácticas

---

## 📞 Soporte

¿Necesitas ayuda? Puedes:

- 📧 Enviar un email a: soporte@smartmind.es
- 🐛 Abrir un issue en GitHub
- 💬 Unirte a nuestro Discord (próximamente)

---

<div align="center">

**⭐ Si este proyecto te ha sido útil, considera darle una estrella en GitHub ⭐**

Hecho con ❤️ para SmartMind

[⬆ Volver arriba](#-verificador-de-prácticas-sepe--smartmind)

</div>
