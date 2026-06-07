import os
from google import genai
from concurrent.futures import ThreadPoolExecutor

# Configuración de los archivos del ecosistema web
ARCHIVOS_PROYECTO = [
    {
        "tipo": "landing_principal",
        "es": "index.html",
        "en": "index_en.html",
        "fr": "index_fr.html"
    },
    {
        "tipo": "ingredientes_lifestyle",
        "es": "lifestyle.html",
        "en": "lifestyle_en.html",
        "fr": "lifestyle_fr.html"
    },
    {
        "tipo": "privacidad_legal",
        "es": "privacy.html",
        "en": "privacy_en.html",
        "fr": "privacy_fr.html"
    }
]

def limpiar_codigo_html(texto_raw):
    """Limpia las etiquetas de formato que devuelve el modelo"""
    texto_limpio = texto_raw.strip()
    if texto_limpio.startswith("```html"):
        texto_limpio = texto_limpio[7:]
    elif texto_limpio.startswith("```"):
        texto_limpio = texto_limpio[3:]
    if texto_limpio.endswith("```"):
        texto_limpio = texto_limpio[:-3]
    return texto_limpio.strip()

def optimizar_y_traducir(contenido_html, tipo_seccion, idioma_destino):
    """Conexión directa con Gemini 3.5 Flash"""
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    if tipo_seccion == "landing_principal":
        enfoque_seo = (
            "Optimiza el cuerpo de texto general y la sección de FAQs. "
            "Redacta las respuestas de las FAQs de forma directa y resolutiva para maximizar "
            "las posibilidades de capturar Featured Snippets en Google Search Console."
        )
    elif tipo_seccion == "ingredientes_lifestyle":
        enfoque_seo = (
            "Enfócate en las descripciones de los ingredientes activos de la bebida. "
            "Potencia la riqueza semántica de sus propiedades de rendimiento, energía y estilo de vida premium."
        )
    elif tipo_seccion == "privacidad_legal":
        enfoque_seo = (
            "Refina y actualiza la política de privacidad siguiendo los estándares de transparencia "
            "de las normativas de la UE (GDPR). Estructura el texto de forma clara y escaneable, "
            "tomando como referencia de diseño corporativo la web de Red Bull."
        )

    prompt = f"""
    Actúas como un Consultor SEO Senior, Copywriter Profesional Nativo y Programador Frontend.
    Tu objetivo es mejorar y adaptar los textos del siguiente código HTML bajo estas directrices: {enfoque_seo}

    REGLAS DE ORO INVIOLABLES:
    1. PROHIBIDO MODIFICAR TÍTULOS: No alteres bajo ningún concepto las etiquetas <title>, <h1> ni textos que definan la identidad principal de la marca (ej. 'THE LIQUID POWER'). Tampoco añadas iniciales o códigos de países a los textos.
    2. HUMANIZACIÓN TOTAL: El tono debe ser sofisticado, natural y fluido. Evita estructuras repetitivas o clichés predecibles de IA. Debe sonar 100% humano.
    3. IDIOMA MANDATORIO DE SALIDA: Todo el contenido textual del HTML debe devolverse perfectamente adaptado al idioma: '{idioma_destino}'.
    4. PRESERVACIÓN DEL CÓDIGO: Mantén intactas las etiquetas HTML, clases de CSS, IDs, scripts, enlaces y rutas de imágenes. Devuelve exclusivamente el código HTML completo resultante sin introducciones ni notas.

    Código HTML a procesar:
    {contenido_html}
    """

    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    return limpiar_codigo_html(response.text)

def tarea_traduccion_paralela(ruta_archivo, html_base_es, tipo_seccion, idioma):
    """Proceso individual para ejecutar en hilos paralelos"""
    if os.path.exists(ruta_archivo):
        print(f"   ➔ [Paralelo] Procesando traducción ({idioma.upper()}): {ruta_archivo}")
        html_optimizado = optimizar_y_traducir(html_base_es, tipo_seccion, idioma)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(html_optimizado)
        print(f"   ✅ [Paralelo] {ruta_archivo} guardado con éxito.")

def ejecutar_seo_orquestado():
    for grupo in ARCHIVOS_PROYECTO:
        archivo_es = grupo["es"]
        
        if not os.path.exists(archivo_es):
            print(f"⚠️ Archivo base no encontrado: {archivo_es}. Saltando grupo.")
            continue

        print(f"\n🚀 Iniciando optimización base en Español: {archivo_es}")
        with open(archivo_es, 'r', encoding='utf-8') as f:
            html_original = f.read()

        # 1. Se optimiza la matriz en Español (punto de partida obligatorio)
        html_es_optimizado = optimizar_y_traducir(html_original, grupo["tipo"], "es")
        with open(archivo_es, 'w', encoding='utf-8') as f:
            f.write(html_es_optimizado)
        print(f"   ✅ Matriz base ({archivo_es}) actualizada.")

        # 2. SE LANZA EL TRABAJO EN PARALELO (Inglés y Francés a la vez)
        print(f"   ⚡ Lanzando traducciones EN y FR en paralelo para {grupo['tipo']}...")
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(tarea_traduccion_paralela, grupo["en"], html_es_optimizado, grupo["tipo"], "en")
            executor.submit(tarea_traduccion_paralela, grupo["fr"], html_es_optimizado, grupo["tipo"], "fr")

if __name__ == "__main__":
    ejecutar_seo_orquestado()