# INF8239_U01
Repositorio  Ciencia de Datos II INF-8239-C2

## Unidad 01: Modelos avanzados, reducción dimensional y Green AI
**Estudiante:** Jhonatan Leandro Cabral Pujols  


# U01.LAB00: Preparación y validación del entorno profesional 
---
### 1. Sistema Operativo y Entorno de Ejecución
- **Entorno de desarrollo:** GitHub Codespaces (Contenedor Cloud basado en Linux)
- **Sistema Operativo:** Linux 6.8.0-1064-azure-x86_64 con glibc 2.39
- **Python:** 3.14.2 (GCC 13.3.0)
- **Intérprete activo:** `/workspaces/INF8239_U01/.venv/bin/python`


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


### 6. Verificación del entorno en Jupyter
- Se ejecutó el notebook notebooks/00_verificacion.ipynb seleccionando el kernel .venv.
- Salida validada mediante aserción sobre sys.executable.

### 7. Registro de Versionado
```bash
git add .
git commit -m "chore: create INF-8239 reproducible environment"
git push
```

# U01.LAB02: Busqueda, seleccion y auditoria de un dataset publico
---
Este repositorio contiene la selección, auditoría, contrato de datos y baseline predictivo para el mantenimiento industrial utilizando el dataset **AI4I 2020 Predictive Maintenance**.

## 1. Instalación y Entorno
El proyecto está optimizado para ejecutarse en VS Code / GitHub Codespaces con Python 3.10+.

```bash
# Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Linux/Codespaces
.venv\Scripts\activate   # En Windows PowerShell

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Descarga Reproducible
Los datos se obtienen directamente del repositorio UCI mediante el script modular en src/inf8239_u01/data.py:

```python
import io
from pathlib import Path
import urllib.request
import zipfile
import pandas as pd


def download_csv(url: str, destination: str = "data/raw/dataset.csv") -> Path:
    if not url.startswith(("https://", "http://")):
        raise ValueError("La fuente debe ser una URL HTTP(S)")

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Si es un archivo ZIP (caso del repositorio UCI)
    if url.endswith(".zip"):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req) as response:
            zip_content = response.read()

        with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
            csv_files = [f for f in z.namelist() if f.endswith(".csv")]
            if not csv_files:
                raise ValueError(
                    "No se encontró ningún archivo CSV dentro del ZIP"
                )
            with z.open(csv_files[0]) as f:
                frame = pd.read_csv(f)
    else:
        frame = pd.read_csv(url)

    if frame.empty:
        raise ValueError("El dataset descargado está vacío")

    frame.to_csv(path, index=False)
    return path
```

## 3. Ejecución en el Notebook (notebooks/02_auditoria_dataset.ipynb)

Para garantizar que el módulo se importe de forma robusta sin importar el directorio de trabajo activo, se incorpora src al sys.path y se resuelve la ruta de destino respecto a la raíz del repositorio:

```python
from pathlib import Path
import sys

# 1. Asegurar que la carpeta 'src' esté en las rutas de importación de Python
PROJECT_ROOT = (
    Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
)
src_dir = PROJECT_ROOT / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# 2. Ahora sí se puede importar directamente
from inf8239_u01.data import download_csv

# 3. Descarga reproducible oficial desde UCI
URL = "[https://archive.ics.uci.edu/static/public/601/ai4i+2020+predictive+maintenance+dataset.zip](https://archive.ics.uci.edu/static/public/601/ai4i+2020+predictive+maintenance+dataset.zip)"
dest_path = PROJECT_ROOT / "data" / "raw" / "dataset.csv"

path = download_csv(URL, destination=str(dest_path))
print("Descarga completada y verificada en:", path)
```

## 4. Definicion del Problema:

- **Target:** Machine failure (0: Operación normal, 1: Falla de la máquina).
- **Métrica Principal:** F1-macro (junto con Recall de la clase minoritaria), debido al marcado desbalance de clases (~3.4% de eventos de falla).
- **Mitigación de Data Leakage:** Se retiraron estrictamente los identificadores (UDI, Product ID) y los modos de falla específicos (TWF, HDF, PWF, OSF, RNF), ya que solo se revelan una vez producida la avería.


## 5. Ejecución del Pipeline y Pruebas:

Notebook principal: Ejecutar notebooks/02_auditoria_dataset.ipynb de inicio a fin.

Pruebas automatizadas (pytest):

```bash
PYTHONPATH=src python -m pytest -q
```

## 6. Conclusión:

> **Conclusión Técnica del Experimento y Auditoría de Datos**
>
> La selección y auditoría rigurosa del conjunto de datos **AI4I 2020 Predictive Maintenance** permitió sentar una base metodológica sólida y reproducible para la toma de decisiones en entornos de manufactura industrial. A través de la auditoría inicial se constató la integridad del archivo sin la presencia de valores ausentes (*missing values*) ni registros duplicados a lo largo de sus 10,000 instancias. No obstante, el desafío central del problema reside en dos dimensiones fundamentales: el severo desbalance de clases y la presencia de variables causales con potencial de fuga de información (*data leakage*).
>
> La variable dependiente `Machine failure` presenta apenas una tasa de incidencia del 3.39% frente a más de un 96% de estados operativos normales. Bajo este contexto, el uso de la exactitud (*accuracy*) como métrica rectora resulta metodológicamente inválido, tal como evidenció el modelo base trivial (*DummyClassifier*). Este clasificador ingenuo, al limitarse a predecir sistemáticamente la clase mayoritaria, obtiene un accuracy superior al 96% pero un **F1-macro inferior a 0.50**, fracasando rotundamente al predecir 0% de los eventos reales de fallo. Por tal motivo, se adoptó el **F1-macro** y el análisis de la matriz de confusión, donde el **falso negativo** representa el error más crítico: ignorar una falla incipiente conlleva roturas catastróficas, tiempos de inactividad imprevistos y costos operativos desproporcionados para la planta.
>
> Asimismo, la fase de saneamiento de variables fue determinante. La exclusión analítica de los identificadores (`UDI` y `Product ID`) evitó sobreajustes espurios por memorización de secuencias, mientras que la eliminación deliberada de los cinco modos de falla (`TWF`, `HDF`, `PWF`, `OSF`, `RNF`) blindó el flujo ante fugas del futuro. Al ser etiquetas que solo se constatan con posterioridad a la interrupción funcional de la máquina, incluirlas en el conjunto de entrenamiento habría provocado un modelo artificialmente perfecto pero inútil en un esquema de telemetría en tiempo real.
>
> Finalmente, la integración del pipeline con `ColumnTransformer` (escalando variables continuas como temperatura, torque y velocidad de giro, y codificando la variante cualitativa de producto) junto a una máquina de soporte vectorial (SVM) con núcleo RBF, demostró la viabilidad de capturar dependencias no lineales complejas entre las tensiones mecánicas y los gradientes térmicos. El establecimiento de pruebas automatizadas mediante `pytest` garantiza que las restricciones dimensionales y semánticas del contrato de datos perduren de manera confiable a lo largo de las iteraciones analíticas posteriores.

# U01.LAB03: Ensambles, Reducción Dimensional (PCA / t-SNE) y Green AI

## 1. Congelar el Protocolo Metodológico

* **Dataset:** AI4I 2020 Predictive Maintenance (UCI).
* **Target:** `Machine failure` (Binario: 0 = Normal, 1 = Falla).
* **Exclusiones de fuga (Data Leakage) e identificadores:** `['UDI', 'Product ID', 'TWF', 'HDF', 'PWF', 'OSF', 'RNF']`.
* **Partición fija:** 80% Entrenamiento (`Xtr`, `ytr`), 20% Prueba (`Xte`, `yte`) con `random_state=42` y estratificación (`stratify=y`). La partición de prueba se mantiene intacta hasta la evaluación final.
* **Métrica principal:** **F1-macro** y **F1 de la clase positiva (1 - Falla)**. Dado el desbalance (~3.4% de fallas), se prioriza penalizar los falsos negativos sin comprometer la eficiencia operativa.
* **Criterio Green AI / Frontera de Pareto:** Evaluación de desempeño frente a tiempo de latencia/entrenamiento y consumo computacional.

## 2. Resumen de Resultados

* **Mejor Clasificador:** `HistGradientBoostingClassifier` (`boost`) dominó la frontera de Pareto con un **F1-macro de 0.9020** y **Recall-macro de 0.8593**.
* **Eficiencia Computacional:** `boost` redujo el tiempo de entrenamiento en más de un 80% respecto a SVM y Random Forest, con una latencia de predicción de 14.4 ms y un tamaño serializado de solo 310 KB.
* **Reducción Dimensional:** PCA al 95% de varianza redujo las 5 variables numéricas a 3 componentes, pero degradó el recall de fallas al 13%, demostrando que la varianza no supervisada no maximiza la separación de anomalías.
* **Archivos generados:**
  * `reports/green_ai_results.csv`: Métricas de rendimiento, tiempos y bandera de Pareto.
  * `reports/tsne_two_seeds.png`: Visualización bidimensional comparativa de variedades con t-SNE.
  * `reports/pareto.png`: Gráfico de dispersión de la frontera de eficiencia Green AI.

## 3. Verificacion Checklist

* Mismo dataset y partición del Ejercicio 01: Sí, división fija estratificada 80/20 sobre AI4I 2020 con semilla 42.
* Al menos seis configuraciones: Sí (logistic, svm_c1, svm_c10, rf_100, rf_300, boost).
* SVM, Random Forest y boosting: Sí, evaluados en el benchmark.
* PCA o alternativa justificada: Sí, integrado y analizado en el paso 4
* Dos t-SNE con semillas distintas: Sí, generado y guardado con semillas 42 y 7 en reports/tsne_two_seeds.png.
* Tres repeticiones temporales y mediana: Sí, calculado mediante las 3 iteraciones de benchmarking.
* Tamaño serializado e inferencia: Sí, reportados en columnas size_kb y predict_ms.
* CSV, figuras, pruebas y README: Sí, green_ai_results.csv, tsne_two_seeds.png, pareto.png y las pruebas unitarias en tests.
* Frontera de Pareto y decisión cuantificada: Sí, función modularizada, probada con tests unitarios y documentada.
