import time
import pandas as pd
from deep_translator import GoogleTranslator

# Leer el dataset en CSV
df = pd.read_csv("./dataset.csv")
print(df.head())

# El dataset contiene algunos problemas matemáticos en el idioma inglés y ruso.
# Section(Russian), Section(English), Question(Russian), Question(English),
# Options(Russian), Option(English), Solution(Russian), Solution(English)

# Pasaremos a eliminar los elementos en ruso y cambiar el nombre de la columna en un formato más claro y accesible

# Opción nro 1: Generarlo en dos pasos para más claridad

# Paso 1: Crear nuevo DataFrame solo con las columnas que necesitamos
new_df = pd.DataFrame(
    {
        "Section(English)": df["Section(English)"],
        "Section(Spanish)": df["Section(English)"],
        "Question(English)": df["Question(English)"],
        "Question(Spanish)": df["Question(English)"],
        "Options(English)": df["Option(English)"],
        "Options(Spanish)": df["Option(English)"],
        "Answer": df["Answer"],
        "Solution(English)": df["Solution(English)"],
        "Solution(Spanish)": df["Solution(English)"],
    }
)

# Paso 2: Renombrar las columnas usando un diccionario de mapeo
column_mapping = {
    "Section(English)": "section_en",
    "Section(Spanish)": "section_es",
    "Question(English)": "question_en",
    "Question(Spanish)": "question_es",
    "Options(English)": "options_en",
    "Options(Spanish)": "options_es",
    "Answer": "answer",
    "Solution(English)": "solution_en",
    "Solution(Spanish)": "solution_es",
}

new_df = new_df.rename(columns=column_mapping)
print(new_df.head())

# Opcion nro. 2: Hacer el proceso en un solo paso

# Crear nuevo DataFrame solo con las columnas en inglés y renombrarlas
new_df2 = pd.DataFrame(
    {
        "section_en": df["Section(English)"],
        "section_es": df["Section(English)"],  # Necesitará traducción
        "question_en": df["Question(English)"],
        "question_es": df["Question(English)"],  # Necesitará traducción
        "options_en": df["Option(English)"],
        "options_es": df["Option(English)"],  # Necesitará traducción
        "answer": df["Answer"],
        "solution_en": df["Solution(English)"],
        "solution_es": df["Solution(English)"],  # Necesitará traducción
    }
)
print(new_df2)

# En este momento se han creado las columnas en español pero asignandole el texto en inglés
# Necesitamos traducirlo, para ello nos apoyaremos en el paquete deep_translator para generar
# una traducción inicial


def translate_text(text):
    try:
        # Esta pausa es necesaria para evitar problemas con los límites en el accesso al API
        time.sleep(0.5)
        return GoogleTranslator(source="en", target="es").translate(text)
    except Exception as e:
        print(f"Error traduciendo: {text[:50]}...")
        print(f"Error: {str(e)}")
        return text


# Traducir cada columna

# Tranducciones las secciones. Como solo son dos secciones, podemos usar un diccionario manual para ello
# Crear diccionario de traducciones manuales para secciones
section_translations = {"Logic": "Lógica", "Algebra": "Álgebra"}
new_df["section_es"] = new_df["section_en"].map(section_translations)

# Traducción de las preguntas
new_df["question_es"] = new_df["question_en"].apply(translate_text)

# Traducción de las opciones
new_df["options_es"] = new_df["options_en"].apply(translate_text)

# Traducción de las soluciones
new_df["solution_es"] = new_df["solution_en"].apply(translate_text)

# Guardar el archivo generado
new_df.to_csv("./math_problems_en_es.csv", index=False)
