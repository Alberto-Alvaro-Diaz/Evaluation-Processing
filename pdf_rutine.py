import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# 1. Cargar dataset de ejemplo
data = {
    "Grupo": ["A", "A", "B", "B", "C", "C"],
    "Quincena": [1, 2, 1, 2, 1, 2],
    "Ventas": [100, 150, 300, 250, 200, 400]
}
df = pd.DataFrame(data)

# 2. Crear un resumen estadístico
resumen = df.groupby(["Grupo", "Quincena"])["Ventas"].sum().reset_index()

# 3. Configuración del PDF
pdf_file = "resumen_dataset.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# 4. Agregar título
elements.append(Paragraph("📊 Resumen del Dataset", styles["Title"]))
elements.append(Spacer(1, 20))

# 5. Agregar estadísticas generales
stats = df.describe(include="all").round(2).to_dict()
elements.append(Paragraph("📌 Estadísticas generales:", styles["Heading2"]))

for col, vals in stats.items():
    elements.append(Paragraph(f"<b>{col}</b>: {vals}", styles["Normal"]))
    elements.append(Spacer(1, 10))

elements.append(Spacer(1, 20))

# 6. Convertir el resumen en tabla
elements.append(Paragraph("📌 Ventas por Grupo y Quincena:", styles["Heading2"]))
table_data = [resumen.columns.tolist()] + resumen.values.tolist()

table = Table(table_data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
]))
elements.append(table)

# 7. Construir PDF
doc.build(elements)
print(f"✅ PDF generado: {pdf_file}")