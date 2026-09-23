# INF8239_U01
Repositorio  Ciencia de Datos II INF-8239-C2

## Unidad 01: Modelos avanzados, reducción dimensional y Green AI
**Estudiante:** Jhonatan Leandro Cabral Pujols  
**Laboratorio:** U01.LAB00 - Preparación y validación del entorno profesional  

---

### 1. Sistema Operativo y Entorno de Ejecución
- **Entorno de desarrollo:** GitHub Codespaces (Contenedor Cloud basado en Linux)
- **Sistema Operativo:** Linux 6.8.0-1064-azure-x86_64 con glibc 2.39
- **Python:** 3.14.2 (GCC 13.3.0)
- **Intérprete activo:** `/workspaces/INF8239_U01/.venv/bin/python`

---

### 2. Comandos Utilizados

#### Configuración de Git
```bash
git config --global user.name "Jhonatan Cabral"
git config --global user.email "prodintdata@gmail.com"
```

### 3. Estructura de carpetas y entorno virtual
```bash
mkdir -p data/raw notebooks reports src/inf8239_u01 tests docs
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalación de dependencias
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Ejecución de pruebas unitarias
```bash
PYTHONPATH=src python -m pytest -q
```
---

### 6. Verificación del entorno en Jupyter
- Se ejecutó el notebook notebooks/00_verificacion.ipynb seleccionando el kernel .venv.
- Salida validada mediante aserción sobre sys.executable.
---
### 7. Registro de Versionado
```bash
git add .
git commit -m "chore: create INF-8239 reproducible environment"
git push
```
