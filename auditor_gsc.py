import os
import json
from google import genai
from google.oauth2 import service_account
from googleapiclient.discovery import build

# =====================================================================
# CONFIGURACIÓN DEL SITIO (Cambia esto por tu dominio real registrado)
# =====================================================================
DOMINIO = "https://originalliquidpower.com/" 

MAPEO_URLS = {
    f"{DOMINIO}index.html": "index.html",
    f"{DOMINIO}index_en.html": "index_en.html",
    f"{DOMINIO}index_fr.html": "index_fr.html",
    f"{DOMINIO}lifestyle.html": "lifestyle.html",
    f"{DOMINIO}lifestyle_en.html": "lifestyle_en.html",
    f"{DOMINIO}lifestyle_fr.html": "lifestyle_fr.html",
    f"{DOMINIO}privacy.html": "privacy.html",
    f"{DOMINIO}privacy_en.html": "privacy_en.html",
    f"{DOMINIO}privacy_fr.html": "privacy_fr.html"
}

def obtener_cliente_gsc():
    """Autenticación segura con la API de Google Search Console"""
    info_claves = json.loads(os.environ["GSC_SERVICE_ACCOUNT_JSON"])
    credenciales = service_account.Credentials.from_service_account_info(info_claves)
    scope = ["https://www.googleapis.com/auth/webmasters.readonly"]
    credenciales_con_scope = credenciales.with_scopes(scope)
    return build("searchconsole", "v1", credentials=credenciales_con_scope)

def limpiar_codigo_html(texto_raw):
    """Limpia los contenedores de markdown que Gemini suele adjuntar al código"""
    texto_limpio = texto_raw.strip()
    if texto_limpio.startswith("```html"): 
        texto_limpio = texto_limpio[7:]
    elif texto_limpio.startswith("```"): 
        texto_limpio = texto_limpio[3:]
    if texto_limpio.endswith("```"): 
        texto_limpio = texto_limpio[:-3]
    return texto_limpio.strip()

def reparar_codigo_con_gemini(archivo_local, informe_error):
    """Gemini analiza el error técnico dictaminado por Google y repara el código local"""
    print(f"   🤖 Activando a Gemini para reparar: {archivo_local}")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    with open(archivo_local, 'r', encoding='utf-8') as f:
        html_actual = f.read()

    prompt = f"""
    Actúas como un Ingeniero SEO Técnico Avanzado y Programador Frontend.
    Google Search Console ha reportado un error de indexación en este archivo.
    
    INFORME DE ERROR DE GOOGLE:
    {json.dumps(informe_error, indent=2)}

    TU MISIÓN:
    Analiza el código HTML actual y soluciona el problema técnico indicado por Google. 
    - Si es un problema de usabilidad móvil: revisa viewports, contenedores desbordados o tamaños de fuentes en Tailwind.
    - Si es un error de indexación/rastreo: busca si hay etiquetas <meta name="robots" content="noindex"> accidentales o enlaces rotos.
    - Mantén intactos el diseño premium, textos y lógicas del resto de la web.
    
    Devuelve única y exclusivamente el código HTML completo corregido, sin introducciones ni bloques de comentarios explicativos.

    CÓDIGO ACTUAL:
    {html_actual}
    """
    
    response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
    codigo_corregido = limpiar_codigo_html(response.text)
    
    with open(archivo_local, 'w', encoding='utf-8') as f:
        f.write(codigo_corregido)
    print(f"   ✅ Archivo {archivo_local} reparado y sobrescrito localmente.")

def ejecutar_auditoria_semanal():
    print("🔍 Iniciando inspección preventiva semanal en Google Search Console...")
    cliente_gsc = obtener_cliente_gsc()

    for url_remota, archivo_local in MAPEO_URLS.items():
        if not os.path.exists(archivo_local):
            continue

        print(f"\n📡 Inspeccionando en GSC: {url_remota}")
        try:
            request_body = {
                "inspectUrl": url_remota,
                "siteUrl": DOMINIO,
                "languageCode": "es"
            }
            # Llamada oficial a la API de Inspección de Google
            resultado = cliente_gsc.urlInspection().index().inspect(body=request_body).execute()
            
            status_result = resultado.get("inspectionResult", {}).get("indexStatusResult", {})
            veredicto = status_result.get("verdict", "UNKNOWN")
            
            print(f"   Verdict de Google: {veredicto}")

            # Si Google detecta errores técnicos graves en la URL
            if veredicto in ["FAIL", "PARTIAL"]:
                print(f"   ⚠️ Alerta técnica detectada en Google para {url_remota}")
                reparar_codigo_con_gemini(archivo_local, status_result)
            else:
                print(f"   ✨ La URL está sana y cumple las políticas de Google.")

        except Exception as e:
            print(f"   ❌ Error al conectar con la API para {url_remota}: {str(e)}")

if __name__ == "__main__":
    ejecutar_auditoria_semanal()