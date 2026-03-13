import google.generativeai as genai
import feedparser
import os
from datetime import datetime

# --- 1. CONFIGURATION API ---
api_key = os.environ.get("GEMINI_OSI") # Assurez-vous que le nom correspond à votre secret GitHub
if not api_key:
    raise ValueError("Clé API introuvable.")
genai.configure(api_key=api_key)

# Recherche du meilleur modèle disponible
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

# --- 2. SOURCING : COLLECTE AUTOMATIQUE DES NEWS VIA RSS ---
print("📡 Collecte des actualités en cours...")

# Liste de flux RSS fiables sur l'IA (Vous pouvez en ajouter d'autres)
rss_feeds = [
    "https://news.google.com/rss/search?q=Intelligence+Artificielle+OR+AI+when:7d&hl=fr&gl=FR&ceid=FR:fr", # Google News FR sur l'IA (7 derniers jours)
    "https://techcrunch.com/category/artificial-intelligence/feed/", # TechCrunch (Marché/Tech)
    "https://huggingface.co/blog/feed.xml" # HuggingFace (Tech/Open Source)
]

news_data = ""
for url in rss_feeds:
    try:
        feed = feedparser.parse(url)
        # On prend les 4 actualités les plus récentes de chaque flux
        for entry in feed.entries[:4]:
            titre = entry.get('title', 'Sans titre')
            lien = entry.get('link', '#')
            # On nettoie un peu le résumé pour ne pas surcharger l'IA
            resume_brut = entry.get('summary', '')[:300] 
            news_data += f"- Titre : {titre}\n  Lien : {lien}\n  Extrait : {resume_brut}...\n\n"
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture du flux {url} : {e}")

if not news_data.strip():
    raise ValueError("Aucune actualité n'a pu être récupérée des flux RSS.")

print("✅ Actualités collectées. Envoi à Gemini pour analyse...")

# --- 3. ANALYSE ET GÉNÉRATION HTML PAR L'IA ---
prompt = f"""
Tu es un expert en veille stratégique. Voici les actualités brutes récoltées ce matin :
{news_data}

Ta mission :
1. Analyse ces actualités et sélectionne les 6 à 9 plus importantes.
2. Classe-les intelligemment dans 3 catégories : GOUVERNANCE (Lois, éthique, procès), MARCHÉ (Business, rachats, entreprises), TECH (Nouveaux modèles, open source, agents).
3. Génère UNIQUEMENT le code HTML contenu à l'intérieur de la balise <main> avec la structure Tailwind demandée.

Structure HTML OBLIGATOIRE pour chaque colonne :
<section>
    <h2 class="text-xl font-bold text-indigo-800 border-b-2 border-indigo-200 mb-4 pb-2">Nom de la Catégorie</h2>
    
    <details class="mb-3 bg-white border border-gray-200 rounded-lg shadow-sm group">
        <summary class="flex justify-between items-center cursor-pointer p-4 font-medium text-sm hover:text-indigo-600 list-none">
            <span class="font-bold truncate pr-4" title="[TITRE]">[EMOJI] [TITRE COURT ET PERCUTANT]</span>
            <span class="text-indigo-500 group-open:rotate-45 transition-transform text-xl flex-shrink-0">+</span>
        </summary>
        <div class="p-4 text-sm bg-gray-50 border-t border-gray-100 text-gray-700">
            <p class="mb-3">[Résumé analytique de l'impact en 2 ou 3 phrases]</p>
            <a href="[LIEN_REEL_DE_L_ARTICLE]" target="_blank" rel="noopener noreferrer" class="text-indigo-600 hover:text-indigo-800 underline font-semibold text-xs">Lire l'article complet →</a>
        </div>
    </details>
</section>

Règle absolue : Utilise impérativement les liens (Lien : http...) fournis dans les données brutes. N'invente aucun lien. Ne mets pas de balises ```html autour de ta réponse.
"""

def main():
    try:
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(prompt)
        new_content = response.text.replace("```html", "").replace("```", "").strip()

        # --- 4. ASSEMBLAGE DU SITE WEB ---
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Veille IA Stratégique</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <link href="[https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap)" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #f3f4f6; }}
        details > summary::-webkit-details-marker {{ display: none; }}
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-7xl mx-auto bg-white rounded-xl shadow-xl p-6 md:p-8 border-t-8 border-indigo-600">
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 border-b pb-6">
            <div>
                <h1 class="text-3xl font-black text-indigo-900 tracking-tight">DASHBOARD VEILLE IA</h1>
                <p class="text-sm text-gray-500 mt-1">Généré de manière autonome par Agent IA - {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
            </div>
            <div class="mt-4 md:mt-0 bg-indigo-50 text-indigo-700 px-4 py-2 rounded-full text-xs font-bold border border-indigo-100 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                Sourcing Automatique Actif
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
        print("✅ SUCCÈS : La veille a été générée, analysée et publiée !")

    except Exception as e:
        print(f"❌ ÉCHEC FINAL : {e}")

if __name__ == "__main__":
    main()