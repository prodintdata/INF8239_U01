# Ficha del dataset
- Dominio: Mantenimiento predictivo en manufactura industrial.
- Unidad de análisis: Una máquina/herramienta durante un ciclo de operación monitorizado (mediciones de temperatura, torque, velocidad y desgaste).
- Decisión: Programar una parada de mantenimiento o reemplazo de herramienta antes de que se produzca una rotura o falla funcional.
- Target: `Machine failure` (`0`: Operación normal, `1`: Falla de máquina).
- Tipo de tarea: Clasificación binaria supervisada.
- Error más costoso: Falso negativo (predecir que la máquina está en estado normal cuando está a punto de fallar), provocando paradas no programadas de la línea de producción, daños a la maquinaria y riesgos para los operarios.
- Usuario: Jefes de planta, supervisores de producción y técnicos de mantenimiento industrial.

## 2. Comparación y selección de candidatos

### Registro de fuentes y enlaces
* **Candidato A (Elegido):** AI4I 2020 Predictive Maintenance Dataset
  * **URL de la ficha:** https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
  * **URL de descarga directa:** https://archive.ics.uci.edu/static/public/601/ai4i+2020+predictive+maintenance+dataset.zip
  * **DOI / Cita:** 10.24432/C5HS5C | Licencia: Creative Commons Attribution 4.0 International (CC BY 4.0)

* **Candidato B (Alternativo):** Bank Marketing
  * **URL de la ficha:** https://archive.ics.uci.edu/dataset/222/bank+marketing
  * **URL de descarga directa:** https://archive.ics.uci.edu/static/public/222/bank+marketing.zip
  * **DOI / Cita:** 10.24432/C5K306 | Licencia: Creative Commons Attribution 4.0 International (CC BY 4.0)

---

### Tabla Comparativa de Criterios

| Criterio | Candidato A (AI4I Predictive Maintenance) | Candidato B (Bank Marketing) |
| :--- | :--- | :--- |
| **Procedencia** | UCI Machine Learning Repository (Donado el 29/08/2020 por Stephan Matzka). | UCI Machine Learning Repository (Donado el 13/02/2012 por S. Moro, P. Rita, P. Cortez). |
| **Licencia** | Creative Commons Attribution 4.0 International (CC BY 4.0). | Creative Commons Attribution 4.0 International (CC BY 4.0). |
| **Filas / Columnas** | 10,000 instancias / 14 columnas (UID, Product ID, Type, 5 señales continuas de sensores y 6 etiquetas de falla). | 45,211 instancias / 17 columnas (variables demográficas, financieras y de contacto). |
| **Target y clases** | Binario: `Machine failure` (`0`: No falla [9,661], `1`: Falla [339]). Desbalance severo (~3.4% fallas). | Binario: `y` (`yes`: Contrata depósito [5,289], `no`: No contrata [39,922]). Desbalance moderado (~11.7%). |
| **Ausentes** | No contiene valores ausentes (0 valores nulos reportados y verificados). | No tiene valores nulos explícitos (`NaN`), pero incluye valores codificados como `"unknown"` en atributos clave. |
| **Riesgo de fuga (*leakage*)** | **Alto si no se audita:** Las columnas `TWF`, `HDF`, `PWF`, `OSF` y `RNF` son los modos de falla específicos que causan directamente `Machine failure`. Deben descartarse de las predictoras para evitar fuga trivial. Además, `UID` y `Product ID` son identificadores únicos sin valor predictivo que deben excluirse. | **Alto en la variable `duration`:** El tiempo de la llamada solo se conoce *después* de que la llamada termina, por lo que incluirla como predictora antes de contactar al cliente genera una fuga temporal irrealizable en producción. |

---

### Justificación de elección
Se selecciona el **Candidato A (AI4I Predictive Maintenance)** debido a:
1. **Alineación con el objetivo del negocio:** Modela directamente la decisión de mantenimiento predictivo formulada en el Paso 1 para evitar paradas críticas no programadas.
2. **Excelente balance dimensional para SVM:** Con 10,000 filas y señales numéricas continuas (temperatura del aire, temperatura del proceso, velocidad de rotación, torque y desgaste de herramienta), permite aplicar escalado y kernels RBF de forma computacionalmente eficiente y rigurosa.

## 3. Aplicación de criterios de aceptación

Se valida el cumplimiento de las condiciones requeridas para el dataset **AI4I 2020 Predictive Maintenance**:

* **Volumen de datos (al menos 500 filas):**
  * **Cumple.** El dataset cuenta con 10,000 instancias registradas, superando holgadamente el umbral mínimo exigido sin demandar procesamiento distribuido.

* **Target observable y representativo (mínimo dos clases):**
  * **Cumple.** La variable objetivo es `Machine failure`, la cual presenta dos clases claramente definidas: `0` (Operación normal) y `1` (Falla de máquina).

* **Permisos y términos de uso (datos permitidos para uso académico):**
  * **Cumple.** Se distribuye formalmente bajo la licencia *Creative Commons Attribution 4.0 International (CC BY 4.0)* desde el repositorio UCI Machine Learning, autorizando explícitamente su uso académico y experimental citando a los autores.

* **Disponibilidad operativa de variables (disponibles al momento de predecir):**
  * **Cumple.** Las mediciones de proceso (`Air temperature [K]`, `Process temperature [K]`, `Rotational speed [rpm]`, `Torque [Nm]` y `Tool wear [min]`) provienen de telemetría de sensores en línea que se conocen en tiempo real antes de que ocurra la detención o ruptura. Se descartan explícitamente los modos específicos de falla (`TWF`, `HDF`, etc.) para asegurar cero fuga de datos (*leakage*).

* **Factibilidad computacional (compatible con CPU/entorno local/Codespaces):**
  * **Cumple.** El archivo en formato tabular ocupa ~510 KB sin comprimir. Esto permite un preprocesamiento inmediato y una búsqueda de hiperparámetros con validación cruzada en cuestión de pocos segundos en CPU sin requerir aceleradores GPU.

* **Restricción de originalidad:**
  * **Cumple.** El dataset fue preseleccionado y registrado formalmente para este proyecto en el entorno de trabajo individual.

  ## 4. Auditoría y Diccionario de Datos del Dataset

| Variable | Significado | Unidad | Fuente | Momento de disponibilidad | Transformación prevista | Riesgo identificado |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`UDI`** | Identificador secuencial del registro. | Entero (1 a 10000) | Registro de log | Al momento de ingesta | **Descartar** | Riesgo de memorización/fuga espuria sin valor predictivo. |
| **`Product ID`** | Identificador de pieza y variante (L/M/H + número de serie). | Texto | Catálogo / Código de barras | Previo al procesamiento | **Descartar** (o extraer solo la variante) | Alta cardinalidad; no generaliza a nuevas piezas. |
| **`Type`** | Variante de calidad del producto (L: bajo 50%, M: medio 30%, H: alto 20%). | Categórica (`L`, `M`, `H`) | Ficha técnica del lote | Previo a la operación | Codificación One-Hot o mapeo ordinal (`L:0, M:1, H:2`) | Desbalance de clases de producto. |
| **`Air temperature [K]`** | Temperatura del aire ambiente generada mediante proceso de paseo aleatorio. | Kelvin (K) | Sensor térmico ambiental | Monitoreo en tiempo real | Estandarización (`StandardScaler`) | Ruido de sensor térmico estacional. |
| **`Process temperature [K]`** | Temperatura generada durante la operación (aire + ~10 K por fricción). | Kelvin (K) | Sensor en cabezal de mecanizado | Monitoreo en tiempo real | Estandarización (`StandardScaler`) | Alta colinealidad con la temperatura del aire. |
| **`Rotational speed [rpm]`** | Velocidad de giro del eje calculada a partir de potencia normalizada. | Revoluciones por minuto (rpm) | Encoder / Tacómetro | Monitoreo en tiempo real | Estandarización (`StandardScaler`) | Posibles valores atípicos por fluctuaciones de carga. |
| **`Torque [Nm]`** | Esfuerzo de torsión ejercido sobre la pieza. | Newton-metro (Nm) | Sensor dinamométrico | Monitoreo en tiempo real | Estandarización (`StandardScaler`) | Correlación inversa estricta con la velocidad de giro. |
| **`Tool wear [min]`** | Minutos acumulados de mecanizado de la herramienta en uso. | Minutos (min) | Contador de tiempo en husillo | Monitoreo en tiempo real | Estandarización (`StandardScaler`) | Reinicios no registrados al cambiar de herramienta. |
| **`Machine failure`** | **Variable objetivo (Target).** Indica si ocurrió alguna falla en el ciclo. | Binario (`0`: Normal, `1`: Falla) | Sistema SCADA / Reporte operativo | Observada al finalizar el ciclo | Convertir a tipo entero / vector objetivo $y$ | Desbalance severo de clases (~3.4% fallas). |
| **`TWF`** | Modo de falla por desgaste de herramienta (*Tool Wear Failure*). | Binario (0/1) | Inspección de fallas | **Posterior a la falla** | **Excluir de X** | **Fuga de datos crítica (*Data Leakage*):** Es un componente directo del target. |
| **`HDF`** | Modo de falla por disipación de calor (*Heat Dissipation Failure*). | Binario (0/1) | Inspección de fallas | **Posterior a la falla** | **Excluir de X** | **Fuga de datos crítica (*Data Leakage*):** Causa directa de la falla. |
| **`PWF`** | Modo de falla por sobrecarga de potencia (*Power Failure*). | Binario (0/1) | Inspección de fallas | **Posterior a la falla** | **Excluir de X** | **Fuga de datos crítica (*Data Leakage*):** Es un submodo del target. |
| **`OSF`** | Modo de falla por sobreesfuerzo (*Overstrain Failure*). | Binario (0/1) | Inspección de fallas | **Posterior a la falla** | **Excluir de X** | **Fuga de datos crítica (*Data Leakage*):** Es un submodo del target. |
| **`RNF`** | Modo de falla aleatoria (*Random Failure*). | Binario (0/1) | Inspección de fallas | **Posterior a la falla** | **Excluir de X** | **Fuga de datos crítica (*Data Leakage*):** Es un submodo del target. |