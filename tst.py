import os
import pandas as pd
import google.generativeai as genai

# Configuración de la API de Gemini
genai.configure(api_key = "")

# Modelo que usaremos
MODEL = "gemini-1.5-flash"

# Definir nombres de columnas (ajústalos según tus excels)
CAMPOS_NUMERICOS = ["Campo num 1", "Campo num 2", "Campo num 3"]
CAMPOS_COMENTARIOS = ["Campo abierto 1", "Campo abierto 2"]
CAMPO_EVALUADOR = "Evaluador"
CAMPO_EVALUADO = "Evaluado"

# Función para resumir comentarios usando Gemini
def resumir_comentarios(comentarios):
    if not comentarios:
        return "Sin comentarios."
    
    prompt = (
        "Resume de forma clara y constructiva las siguientes opiniones "
        "que distintos monitores han dado sobre un compañero de campamento. "
        "Incluye fortalezas y áreas de mejora:\n\n"
        + "\n".join(f"- {c}" for c in comentarios)
    )
    
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    # Cargar todos los Excel del directorio actual
    import glob
    all_files = all_files = glob.glob(os.path.join("evaluaciones", "*.xlsx"))

    if not all_files:
        print("⚠️ No se encontraron archivos .xlsx en el directorio.")
        return

    # Leer y unir todos los excels
    df = pd.concat([pd.read_excel(f) for f in all_files], ignore_index=True)

    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    # Procesar evaluaciones por persona evaluada
    for evaluado, grupo in df.groupby(CAMPO_EVALUADO):
        # Calcular medias numéricas
        medias = {}
        for campo in CAMPOS_NUMERICOS:
            if campo in grupo.columns:
                medias[campo] = pd.to_numeric(grupo[campo], errors="coerce").mean()

        # Juntar comentarios de todos los campos abiertos
        comentarios = []
        for campo in CAMPOS_COMENTARIOS:
            if campo in grupo.columns:
                comentarios.extend(grupo[campo].dropna().astype(str).tolist())

        resumen = resumir_comentarios(comentarios)

        # Crear dataframe de salida
        salida = pd.DataFrame({
            "Campo": list(medias.keys()) + ["Resumen de comentarios"],
            "Valor": list(medias.values()) + [resumen]
        })

        # Guardar archivo Excel personalizado
        os.makedirs("resultados", exist_ok=True)
        salida.to_excel(os.path.join("resultados", f"evaluacion_{evaluado}_tst.xlsx"), index=False)
        print(f"✅ Archivo generado: evaluacion_{evaluado}.xlsx")

if __name__ == "__main__":
    main()
