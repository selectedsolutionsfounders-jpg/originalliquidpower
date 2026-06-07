import os
import google.generativeai as genai

# Configurar Gemini
client = genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def ejecutar_seo():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    prompt = f"Actúa como experto SEO. Optimiza el <title> y <meta description> de este HTML. Devuelve solo el HTML completo y corregido: {html}"
    
    response = model.generate_content(prompt)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(response.text.replace("```html", "").replace("```", ""))

if __name__ == "__main__":
    ejecutar_seo()