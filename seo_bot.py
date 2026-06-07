import os
from google import genai

def ejecutar_seo():
    # 1. Leemos tu archivo HTML
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    prompt = f"Actúa como experto SEO. Optimiza el <title> y <meta description> de este HTML. Devuelve solo el HTML completo y corregido: {html}"

    # 2. Nos conectamos con la nueva librería usando tu clave secreta
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    # 3. Llamamos al modelo
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    # 4. Limpiamos el texto devuelto y sobreescribimos el archivo
    nuevo_html = response.text.replace("```html", "").replace("```", "").strip()

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(nuevo_html)

if __name__ == "__main__":
    ejecutar_seo()