import google.generativeai as genai
import os
from datetime import datetime

# Configuration
api_key = os.environ.get("GEMINI_OSI")
if not api_key:
    raise ValueError("La clé API n'est pas trouvée dans les variables d'environnement")

genai.configure(api_key=api_key)

# --- BLOC DIAGNOSTIC ---
print("🔍 ANALYSE DES MODÈLES DISPONIBLES POUR VOTRE CLÉ...")
available_models = []
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            clean_name = m.name.replace('models/', '')
            print(f" - ✅ Disponible : {clean_name}")
            available_models.append(clean_name)
except Exception as e:
    print(f"⚠️ Impossible de lister les modèles : {e}")

# --- SÉLECTION INTELLIGENTE ---
model_preference = ['gemini-1.5-flash', 'gemini-1.5-flash-001', 'gemini-2.5-flash', 'gemini-1.0-pro']
selected_model = 'gemini-pro'

for m in model_preference:
    if m in available_models:
        selected_model = m
        break

print(f"🤖 MODÈLE CHOISI : {selected_model}")
# -----------------------

# --- SOURCES ET LIENS RÉELS ---
# On fournit ici les mots-clés ET les liens que l'IA doit utiliser
sources_context = """
- Gouvernance : La France attaque Grok en justice pour contenus sexistes (Lien: https://lemonde.fr). Régulations IA 2026 (Lien: https://reuters.com/technology).
- Marché : Acquisitions de l'infrastructure par NVIDIA et Meta (Lien: https://techcrunch.com). Consolidation du marché de l'IA (Lien: https://wsj.com).
- Tech : Nouveaux modèles Open Source GLM-4.7 et MiniMax 2.1 sur HuggingFace (Lien: https://huggingface.co). Tendances Vibe Coding et Agents (Lien: https://linkedin.com).
"""

# --- PROMPT STRICT POUR LES ACCORDÉONS ---
prompt = f"""
Tu es un expert en veille stratégique IA. Utilise le contexte et les liens suivants : {sources_context}.
Génère UNIQUEMENT le code HTML contenu à l'intérieur de la balise <main>.

Structure le rendu en 3 colonnes exactes. Pour chaque colonne, crée cette structure :
<section>
    <h2 class="text-xl font-bold text-indigo-800 border-b-2 border-indigo-200 mb-4 pb-2">Nom de la Catégorie</h2>
    </section>

Pour CHAQUE article, tu DOIS obligatoirement utiliser cette structure d'accordéon cliquable :
<details class="mb-3 bg-white border border-gray-200 rounded-lg shadow-sm group">
    <summary class="flex justify-between items-center cursor-pointer p-4 font-medium text-sm hover:text-indigo-600 list-none">
        <span class="font-bold">[EMOJI] Titre de l'actualité</span>
        <span class="text-indigo-500 group-open:rotate-45 transition-transform text-xl">+</span>
    </summary>
    <div class="p-4 text-sm bg-gray-50 border-t border-gray-100 text-gray-700">
        <p class="mb-3">Résumé de l'actualité (2 phrases max).</p>
        <a href="[URL_FOURNIE_DANS_LE_CONTEXTE]" target="_blank" class="text-indigo-600 hover:text-indigo-800 underline font-semibold text-xs">Lire la source originale →</a>
    </div>
</details>

Règle absolue : N'utilise pas de balises markdown ```html. Renvoie directement le code brut.
"""

def main():
    try:
        model = genai.GenerativeModel(selected_model)
        
        response = model.generate_content(prompt)
        new_content = response.text.replace("```html", "").replace("```", "").strip()

        # --- TEMPLATE HTML MODERNE (Style Image 2) ---
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Veille IA</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap)" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; }}
        /* Masquer la petite flèche par défaut des accordéons */
        details > summary::-webkit-details-marker {{ display: none; }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto bg-white rounded-xl shadow-xl p-6 md:p-8 border-t-8 border-indigo-600">
        
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 border-b pb-6">
            <div>
                <h1 class="text-3xl font-black text-indigo-900 tracking-tight">DASHBOARD VEILLE IA</h1>
                <p class="text-sm text-gray-500 mt-1">Généré par Agent IA - {datetime.now().strftime('%d/%m/%Y')}</p>
            </div>
            <div class="mt-4 md:mt-0 bg-indigo-50 text-indigo-700 px-4 py-2 rounded-full text-xs font-bold border border-indigo-100 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                Mise à jour automatique : ON
            </div>
        </header>

        <main class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {new_content}
        </main>
        
    </div>
</body>
</html>"""
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ SUCCÈS : Site mis à jour avec le nouveau design !")

    except Exception as e:
        print(f"❌ ÉCHEC FINAL : {e}")
        pass

if __name__ == "__main__":
    main()