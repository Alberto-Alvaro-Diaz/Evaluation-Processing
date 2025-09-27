import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Loading environmnet variables
load_dotenv() 
API_KEY = os.getenv('API_KEY_OPEN') 

# Inicializar cliente de OpenAI
client = OpenAI(api_key = API_KEY)

# Carpeta donde están los ficheros Excel
INPUT_FOLDER = "evaluaciones"
OUTPUT_FOLDER = "resultados"

# Campos del Excel
CAMPO_EVALUADO = "Evaluado"  # columna con la persona evaluada
CAMPOS_NUMERICOS = ["Campo num 1", "Campo num 2", "Campo num 3"]
CAMPOS_ABIERTOS = ["Campo abierto 1","Campo abierto 2"]

# Función para resumir comentarios con OpenAI
def resumir_comentarios(comentarios: list[str]) -> str:
    if not comentarios:
        return "No hay comentarios disponibles."
    
    texto = "\n".join(comentarios)
    prompt = (
        "A continuación tienes las opiniones que varias personas han dado sobre un monitor. "
        "Redáctame un resumen claro y constructivo, incluyendo fortalezas y aspectos a mejorar:\n\n"
        f"{texto}\n\nResumen:"
    )
    
    response = client.chat.completions.create(
    
        model = "gpt-3.5-turbo",  # puedes cambiar por otro modelo
        messages = [{"role": "user", "content": prompt}],
        temperature = 0.5,
    )
    
    return response.choices[0].message.content.strip()

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Cargar todos los Excel de la carpeta
    all_files = [os.path.join(INPUT_FOLDER, f) for f in os.listdir(INPUT_FOLDER) if f.endswith(".xlsx")]
    df = pd.concat([pd.read_excel(f) for f in all_files], ignore_index=True)

    # Agrupar por monitor evaluado
    for evaluado, grupo in df.groupby(CAMPO_EVALUADO):
        # Calcular medias numéricas
        medias = grupo[CAMPOS_NUMERICOS].mean().to_dict()

        # Resumir comentarios
        comentarios = grupo[CAMPOS_ABIERTOS].fillna("").agg(" ".join, axis=1).tolist()
        resumen = resumir_comentarios(comentarios)

        # Crear DataFrame de salida
        data = {**medias, "Resumen": resumen}
        df_out = pd.DataFrame([data])

        # Guardar en Excel
        filename = os.path.join(OUTPUT_FOLDER, f"{evaluado}.xlsx")
        df_out.to_excel(filename, index=False, engine="openpyxl")
        print(f"Generado: {filename}")

if __name__ == "__main__":
    main()