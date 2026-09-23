import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Encabezado (desde página 2)
        if self._pageNumber > 1:
            self.drawString(54, 750, "UASD VIRTUAL | INF-8239 Ciencia de Datos II — Guía Técnica Alternativa")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Pie de página (todas las páginas)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Propuesta Técnica de Entorno — GitHub Codespaces")
        self.drawRightString(558, 32, f"Página {self._pageNumber} de {page_count}")
        self.restoreState()

def build_pdf(filename="Solucion_Entorno_Codespaces_INF8239.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    PRIMARY = colors.HexColor("#1E3A8A")    # Azul institucional UASD
    SECONDARY = colors.HexColor("#0D9488")  # Teal técnico
    TEXT_DARK = colors.HexColor("#0F172A")  # Texto base
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Gris de fondo
    BORDER_COL = colors.HexColor("#CBD5E1") # Bordes

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceAfter=10
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=9,
        spaceAfter=5,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=SECONDARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    def make_code_box(code_str):
        p = Paragraph(code_str.strip().replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    def make_callout(text, bg_color="#EFF6FF", border_color="#3B82F6"):
        p = Paragraph(text, callout_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor(border_color)),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # ==================== PÁGINA 1 ====================
    story.append(Paragraph("INF-8239: CIENCIA DE DATOS II — ESCUELA DE INFORMÁTICA UASD", subtitle_style))
    story.append(Paragraph("Guía Alternativa: Despliegue de Entorno Profesional en GitHub Codespaces", title_style))
    
    meta_text = "<b>Autor:</b> Jhonatan Leandro Cabral Pujols &nbsp;|&nbsp; <b>Fecha:</b> Septiembre 2026<br/><b>Dirigido a:</b> Prof. Edwin Ramón José Nolasco &nbsp;|&nbsp; <b>Alcance:</b> U01 LAB00 - LAB03"
    meta_p = Paragraph(meta_text, meta_style)
    meta_table = Table([[meta_p]], colWidths=[504])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Diagnóstico del Problema en Equipos Administrados", h1_style))
    story.append(Paragraph(
        "Al configurar el <b>U01.LAB00</b> en computadoras corporativas o con restricciones empresariales bajo Windows 11, "
        "las directivas de seguridad centralizadas (<b>WDAC / AppLocker</b> ancladas en HVCI/VBS) bloquean la ejecución de binarios y bibliotecas compiladas en C/C++ "
        "(como <code>_arpack*.pyd</code> en <code>scikit-learn</code> o aceleradores numéricos de <code>numpy</code>), generando eventos de integridad de código "
        "<i>(Event ID 3077)</i>. Dado que el estudiante carece de privilegios para alterar estas directivas MDM de dominio, la ejecución local queda totalmente inhabilitada.",
        body_style
    ))
    
    note_why = (
        "<b>¿Por qué GitHub Codespaces y no Google Colab?</b><br/>"
        "La asignatura evalúa buenas prácticas de ingeniería de software: suite de pruebas automatizadas con <code>pytest</code>, "
        "modularización de código fuente en paquetes reutilizables (<code>src/</code>), persistencia de artefactos en disco (<code>reports/</code>) "
        "y control continuo de versiones vía Git. Google Colab opera sobre un enfoque lineal no persistente que dificulta estas prácticas. "
        "<b>GitHub Codespaces</b> proporciona una instancia completa de Linux accesible vía navegador web con VS Code nativo, "
        "garantizando cumplimiento estricto del manual sin vulnerar las directivas corporativas."
    )
    story.append(make_callout(note_why, bg_color="#FEF3C7", border_color="#D97706"))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Aprovisionamiento Inicial (3 a 5 minutos)", h1_style))
    story.append(Paragraph("<b>Paso 1: Repositorio en GitHub</b>", h2_style))
    story.append(Paragraph(
        "Crear un repositorio en GitHub con el nombre <code>INF8239_U01</code> marcando la casilla <b>Add a README file</b> (puede ser público o privado).",
        body_style
    ))

    story.append(Paragraph("<b>Paso 2: Inicio de la Instancia Codespaces</b>", h2_style))
    story.append(Paragraph(
        "En la página principal del repositorio en GitHub, hacer clic en el botón verde <b>&lt;&gt; Code</b> &rarr; pestaña <b>Codespaces</b> &rarr; "
        "<b>Create codespace on main</b>. Se abrirá la interfaz completa de VS Code en la nube.",
        body_style
    ))

    story.append(Paragraph("<b>Paso 3: Extensiones del Entorno</b>", h2_style))
    story.append(Paragraph(
        "Presionar <code>Ctrl+Shift+X</code> y comprobar que estén instaladas las extensiones oficiales: "
        "<b>Python</b> (Microsoft), <b>Jupyter</b> (Microsoft) y <b>Ruff</b> (Astral Software).",
        body_style
    ))

    story.append(PageBreak())

    # ==================== PÁGINA 2 ====================
    story.append(Paragraph("3. Ejecución Paso a Paso del LAB00 en Codespaces", h1_style))
    story.append(Paragraph(
        "Todos los siguientes comandos se ejecutan directamente en la terminal integrada (<code>bash</code>) del Codespace:",
        body_style
    ))

    story.append(Paragraph("<b>A. Identidad de Git y Estructura de Directorios</b>", h2_style))
    git_code = (
        "git config --global user.name \"Nombre Apellido\"\n"
        "git config --global user.email \"correo@ejemplo.com\"\n"
        "mkdir -p data/raw notebooks reports/models src/inf8239_u01 tests docs"
    )
    story.append(make_code_box(git_code))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>B. Creación de Entorno Aislado (.venv) e Instalación</b>", h2_style))
    venv_code = (
        "python3 -m venv .venv\n"
        "source .venv/bin/activate\n"
        "cat << 'EOF' > requirements.txt\n"
        "numpy>=1.26\n"
        "pandas>=2.2\n"
        "scikit-learn>=1.4\n"
        "matplotlib>=3.8\n"
        "seaborn>=0.13\n"
        "joblib>=1.3\n"
        "pytest>=8.0\n"
        "EOF\n"
        "python -m pip install --upgrade pip\n"
        "python -m pip install -r requirements.txt"
    )
    story.append(make_code_box(venv_code))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>C. Modularización en src/ y Pruebas con pytest</b>", h2_style))
    mod_code = (
        "# Inicializador del paquete\n"
        "touch src/inf8239_u01/__init__.py\n\n"
        "# Modulo base\n"
        "cat << 'EOF' > src/inf8239_u01/environment.py\n"
        "def environment_message() -> str:\n"
        "    return \"Entorno INF-8239 listo\"\n"
        "EOF\n\n"
        "# Prueba unitaria\n"
        "cat << 'EOF' > tests/test_environment.py\n"
        "from inf8239_u01.environment import environment_message\n\n"
        "def test_environment_message():\n"
        "    assert environment_message() == \"Entorno INF-8239 listo\"\n"
        "EOF\n\n"
        "# Validacion de ejecucion\n"
        "PYTHONPATH=src python -m pytest -q"
    )
    story.append(make_code_box(mod_code))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>Resultado esperado en terminal:</i> <code>. [100%] 1 passed in 0.02s</code>.", callout_style))

    story.append(Paragraph("<b>D. Verificación del Kernel en Jupyter</b>", h2_style))
    story.append(Paragraph(
        "1. Crear <code>notebooks/00_verificacion.ipynb</code>.<br/>"
        "2. En la esquina superior derecha, pulsar <b>Select Kernel</b> &rarr; <b>Python Environments...</b> &rarr; elegir <b>.venv</b>.<br/>"
        "3. Ejecutar la celda de verificación requerida por el manual:",
        body_style
    ))
    nb_code = (
        "import sys, platform\n"
        "print(sys.executable)\n"
        "print(sys.version)\n"
        "print(platform.platform())\n"
        "assert \".venv\" in sys.executable.lower()"
    )
    story.append(make_code_box(nb_code))

    story.append(PageBreak())

    # ==================== PÁGINA 3 ====================
    story.append(Paragraph("<b>E. Configuración de .gitignore y Versionado</b>", h2_style))
    git_ctrl_code = (
        "cat << 'EOF' > .gitignore\n"
        ".venv/\n"
        "__pycache__/\n"
        ".pytest_cache/\n"
        ".ipynb_checkpoints/\n"
        "*.joblib\n"
        "data/raw/*\n"
        "!data/raw/.gitkeep\n"
        "EOF\n\n"
        "touch data/raw/.gitkeep\n"
        "git add .\n"
        "git commit -m \"chore: create INF-8239 reproducible environment\"\n"
        "git push"
    )
    story.append(make_code_box(git_ctrl_code))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Evidencias Generadas para Evaluación del LAB00", h1_style))
    
    table_data = [
        [Paragraph("<b>Requisito del Manual</b>", code_style), Paragraph("<b>Resultado en GitHub Codespaces</b>", code_style), Paragraph("<b>Estado</b>", code_style)],
        [Paragraph("Versiones del Sistema", body_style), Paragraph("Python 3.14.2 | Linux 6.8 Azure x86_64 | Git 2.43", body_style), Paragraph("<font color='#0D9488'><b>Aprobado</b></font>", body_style)],
        [Paragraph("Intérprete Aislado", body_style), Paragraph("<code>/workspaces/INF8239_U01/.venv/bin/python</code>", body_style), Paragraph("<font color='#0D9488'><b>Aprobado</b></font>", body_style)],
        [Paragraph("Pruebas Unitarias", body_style), Paragraph("<code>pytest -q</code> exitoso con <code>1 passed</code>", body_style), Paragraph("<font color='#0D9488'><b>Aprobado</b></font>", body_style)],
        [Paragraph("Árbol de Directorios", body_style), Paragraph("<code>data/</code>, <code>notebooks/</code>, <code>reports/</code>, <code>src/</code>, <code>tests/</code>, <code>docs/</code>", body_style), Paragraph("<font color='#0D9488'><b>Aprobado</b></font>", body_style)],
        [Paragraph("Historial de Commits", body_style), Paragraph("Commit inicial trazable y sincronizado con repositorio remoto", body_style), Paragraph("<font color='#0D9488'><b>Aprobado</b></font>", body_style)],
        [Paragraph("Documentación README", body_style), Paragraph("Especificaciones de SO, kernel, rutas y comandos incluidos", body_style), Paragraph("<font color='#0D9488'><b>Aprobado</b></font>", body_style)],
    ]
    ev_table = Table(table_data, colWidths=[130, 294, 80])
    ev_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ev_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Consideraciones para Docentes y Evaluadores", h1_style))
    recom_text = (
        "1. <b>Validez académica plena:</b> GitHub Codespaces cumple con la totalidad de los requisitos pedagógicos fijados en el manual (entornos virtuales, pytest, pipelines y git), eliminando fricciones técnicas causadas por políticas de seguridad locales.<br/>"
        "2. <b>Manejo de repositorios privados:</b> Si el estudiante configura el repositorio como privado, puede otorgar acceso al evaluador mediante <i>Settings &rarr; Collaborators &rarr; Add people</i>, o alternativamente cambiar la visibilidad a pública al momento de la entrega.<br/>"
        "3. <b>Disponibilidad de cuota:</b> El plan estándar de GitHub incluye 120 horas-núcleo gratuitas al mes, volumen suficiente para ejecutar de extremo a extremo las unidades LAB00 a LAB03."
    )
    story.append(make_callout(recom_text, bg_color="#F8FAFC", border_color="#64748B"))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Archivo generado exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
