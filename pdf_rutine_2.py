from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os 

def creating_pdf(nombre_persona: str, valores: dict, comentario: str, output_path: str = os.getcwd()):

    # === Configuración del PDF ===
    os.makedirs(output_path, exist_ok=True)
    pdf_file = os.path.join(output_path, f"evaluacion_{nombre_persona}.pdf")
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # === Título principal ===
    titulo = Paragraph("📊 Informe de Evaluación", styles["Title"])
    elements.append(titulo)
    elements.append(Spacer(1, 20))

    # === Nombre de la persona ===
    nombre = Paragraph(f"<b>Nombre:</b> {nombre_persona}", styles["Heading2"])
    elements.append(nombre)
    elements.append(Spacer(1, 20))

    # === Tabla con cualidades ===
    tabla_data = [
        [Paragraph(str(k), styles["Normal"]), Paragraph(str(v), styles["Normal"])]
        for k, v in valores.items()
    ]

    # Encabezado
    tabla_data.insert(0, ["Cualidad", "Valor"])

    tabla = Table(tabla_data, colWidths=[300, 100])  # puedes ajustar el ancho
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # centra verticalmente
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(tabla)
    elements.append(Spacer(1, 30))

    # === Recuadro grande con comentario ===
    comentario_style = ParagraphStyle(
        "Comentario",
        parent=styles["Normal"],
        backColor=colors.whitesmoke,
        borderWidth=1,
        borderColor=colors.black,
        borderPadding=10,
        leading=15,
    )
    comentario_paragraph = Paragraph(comentario, comentario_style)
    elements.append(comentario_paragraph)

    # === Construir PDF ===
    doc.build(elements)
    print(f"✅ PDF generado: {pdf_file}")


if __name__ == "__main__":
    # === Datos de ejemplo ===
    nombre_persona = "Juan Pérez"
    valores = {
        "Creatividad": 3.5,
        "Trabajo en equipo": 4.2,
        "Liderazgo": 3.8,
        "Responsabilidad": 4.7
    }
    comentario = """
    Juan ha demostrado un buen desempeño en general.<br/><br/>s
    Destaca en su capacidad de colaborar con otros y mantener un compromiso sólido con sus responsabilidades. 
    Su liderazgo está en crecimiento y su creatividad le permite aportar ideas nuevas en distintos contextos.
    """

    creating_pdf(nombre_persona, valores, comentario)
