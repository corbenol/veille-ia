import google.generativeai as genai
import os
from datetime import datetime

# 1. Configuration avec la nouvelle bibliothèque 2026
api_key = os.environ.get("GEMINI_OSI")
genai.configure(api_key=api_key)

# 2. Vos sources
sources_context = """
- Reuters & Le Monde : Suivi des régulations IA et procès Grok en France.
- LinkedIn & X : Tendance sur les agents autonomes et le "Vibe Coding".
- HuggingFace : Sorties des modèles GLM-4.7 et MiniMax 2.1.
- Marché : Acquisitions par NVIDIA, Alphabet et Meta.
"""

# 3. Le Prompt
prompt = f"""Génère UNIQUEMENT le code HTML contenu à l'intérieur de la balise <main> pour un tableau de bord de veille IA.
Utilise Tailwind CSS avec 3 colonnes, des cartes avec la classe 'neo-card' (bordure noire 2px, ombre portée).
Thèmes : {sources_context}. Date : {datetime.now().strftime('%d/%m/%Y')}.
"""

def main():
    try:
        # Utilisation du modèle 'gemini-2.0-flash' (standard en 2026)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(prompt)
        new_content = response.text

        # Nettoyage
        new_content = new_content.replace("```html", "").replace("```", "").strip()

        full_html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Veille IA </title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <style>
        .neo-card {{ border: 2px solid #000; box-shadow: 5px 5px 0px #000; transition: all 0.2s; }}
        .neo-card:hover {{ transform: translate(-2px, -2px); box-shadow: 7px 7px 0px #000; }}
    </style>
</head>
<body class="bg-gray-50 text-gray-900 p-6">
    <header class="max-w-6xl mx-auto mb-12">
        <h1 class="text-4xl font-black uppercase tracking-tighter border-b-4 border-black inline-block mb-4">🤖 Veille IA 2026</h1>
        <p class="text-lg text-gray-600">Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y')}</p>
    </header>
    <main class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        {new_content}
    </main>
</body>
</html>
"""
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ index.html mis à jour !")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()