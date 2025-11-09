Aquí tienes el README completo en un único bloque:

# 🧠 Verificador de Prácticas — SmartMind

Aplicación desarrollada en **Python + Streamlit** para automatizar la verificación de las horas de prácticas de los alumnos en empresas colaboradoras, comparando los datos de fichajes con los módulos cursados y los informes del SEPE.

Permite calcular automáticamente el **porcentaje de asistencia por módulo**, verificar si cada alumno supera el **75 % obligatorio**, y generar un informe compatible con la plantilla oficial del SEPE.

---

## 📦 Requisitos del sistema

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- 🐍 **Python 3.10 o superior** → [Descargar Python](https://www.python.org/downloads/)
- 💻 **Visual Studio Code** → [Descargar VS Code](https://code.visualstudio.com/)
- 🧩 **Git** → [Descargar Git](https://git-scm.com/download/win)
- (Opcional) **Anaconda** o **virtualenv** para crear un entorno aislado

---

## ⚙️ Instalación paso a paso

### 1️⃣ Clonar el repositorio

Abre la terminal (PowerShell o Git Bash) y ejecuta:

```bash
git clone https://github.com/AranchaFF/verificador_practicas.git
cd verificador_practicas

2️⃣ Crear y activar un entorno virtual
# Crear entorno virtual llamado .venv
python -m venv .venv

# Activar entorno virtual en Windows
.\.venv\Scripts\activate

# Activar entorno virtual en Linux / macOS
source .venv/bin/activate

3️⃣ Instalar las dependencias necesarias
# Instalar paquetes requeridos
pip install streamlit pandas openpyxl Pillow

# Crear requirements.txt para futuras instalaciones
pip freeze > requirements.txt

# Alternativamente, si ya tienes requirements.txt
pip install -r requirements.txt

📂 Estructura del proyecto
verificador_practicas/
│
├── app.py                     # Interfaz principal de Streamlit
├── src/
│   ├── analizador_fichajes.py # Lógica de análisis de fichajes
│   ├── generador_informes.py  # Genera el Excel con porcentajes
│   └── utils.py               # Funciones auxiliares
│
├── data/
│   ├── alumnos.xlsx           # Datos de alumnos, módulos y horas totales
│   ├── sepe_plantilla.xlsx    # Plantilla del SEPE
│   └── fichajes.zip           # Fichajes de ejemplo (archivos TXT)
│
├── README.md                  # Documentación del proyecto
└── requirements.txt           # Dependencias del entorno

🚀 Ejecución de la aplicación

Desde la carpeta raíz del proyecto, ejecuta:

streamlit run app.py


Esto abrirá la interfaz web en tu navegador en:

👉 http://localhost:8501

🧮 Uso paso a paso

Sube los archivos de datos desde la interfaz:

alumnos.xlsx

sepe_plantilla.xlsx

fichajes.zip

Pulsa “Analizar fichajes”.

El sistema calculará automáticamente:

Horas totales trabajadas por alumno y módulo.

Porcentaje de asistencia sobre las horas planificadas.

Si cumple o no el mínimo del 75 % exigido.

Descarga el resultado final en formato Excel compatible con el SEPE.

🧪 Archivos de ejemplo incluidos
alumnos.xlsx
ID	Nombre	Empresa_asignada	Módulo	Horas_totales
A001	Ana Pérez	TechData SL	M1	100
A001	Ana Pérez	TechData SL	M2	80
A002	Luis García	Informática Norte	M1	120
A002	Luis García	Informática Norte	M2	60
A003	María López	Sistemas Avanzados	M1	100
sepe_plantilla.xlsx
Nombre	DNI	Curso	Modulo_M1_%	Modulo_M2_%
Ana Pérez	12345678A	Ciberseguridad		
Luis García	87654321B	Ciberseguridad		
María López	11223344C	Ciberseguridad		
fichajes.zip

Contiene archivos de texto como:

A001_fichaje_01.txt
A001_fichaje_M2_01.txt
A002_fichaje_01.txt
A002_fichaje_M2_01.txt
...


Cada archivo incluye los datos de empresa, módulo, horas de entrada y salida del alumno.

🧰 Tecnologías utilizadas

Python 3.11

Streamlit — Interfaz web interactiva

Pandas — Análisis de datos

OpenPyXL — Manipulación de archivos Excel

Pillow — Soporte para imágenes de fichajes (si se usan)

🧾 Ejemplo de resultado
Nombre	DNI	Curso	Modulo_M1_%	Modulo_M2_%	Cumple_75%
Ana Pérez	12345678A	Ciberseguridad	78%	92%	✅
Luis García	87654321B	Ciberseguridad	100%	70%	❌
María López	11223344C	Ciberseguridad	55%	-	❌
🔒 Validaciones y controles

Verificación automática de nombre del alumno, módulo y empresa.

Detección de fichajes con formato erróneo o incompleto.

Cálculo real de horas trabajadas según fichajes diarios.

Control de mínimos del 75 % por módulo.

🧱 Mejoras futuras

Carga de imágenes de fichajes (PDF o JPG).

Panel de administración con historial.

Exportación de informes en PDF.

Conexión con bases de datos (SQLite o PostgreSQL).

📜 Licencia

Proyecto interno de SmartMind / Informática Movifer.
Uso autorizado únicamente para fines educativos o administrativos relacionados con el SEPE.