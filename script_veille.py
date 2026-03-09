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
            # On nettoie le nom (enlève 'models/') pour l'affichage
            clean_name = m.name.replace('models/', '')
            print(f" - ✅ Disponible : {clean_name}")
            available_models.append(clean_name)
except Exception as e:
    print(f"⚠️ Impossible de lister les modèles : {e}")

# --- SÉLECTION INTELLIGENTE ---
# On essaie les modèles dans l'ordre de préférence
model_preference = ['gemini-1.5-flash', 'gemini-1.5-flash-001', 'gemini-2.5-flash', 'gemini-1.0-pro']
selected_model = 'gemini-pro' # Fallback par défaut (le plus vieux et le plus stable)

for m in model_preference:
    if m in available_models:
        selected_model = m
        break

print(f"🤖 MODÈLE CHOISI : {selected_model}")
# -----------------------

sources_context = """
- Reuters & Le Monde : Suivi des régulations IA.
- LinkedIn & X : Vibe Coding et Agents.
- HuggingFace : Modèles GLM-4.7.
- Marché : NVIDIA, Alphabet, Meta.
"""

prompt = f"Génère UNIQUEMENT le code HTML du <body> (sans balise body, juste le contenu div/main) pour un tableau de bord veille IA. Style Tailwind, 3 cartes 'neo-card'. Thèmes: {sources_context}. Date: {datetime.now().strftime('%d/%m/%Y')}."

def main():
    try:
        # Initialisation du modèle choisi dynamiquement
        model = genai.GenerativeModel(selected_model)
        
        response = model.generate_content(prompt)
        new_content = response.text.replace("```html", "").replace("```", "").strip()

        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Veille IA </title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>.neo-card {{ border: 2px solid #000; box-shadow: 5px 5px 0px #000; }}</style>
</head>
<body class="bg-gray-50 p-6">
    <header class="mb-8"><h1 class="text-3xl font-black border-b-4 border-black inline-block">VEILLE IA AUTO</h1></header>
    <main class="grid gap-6">
        {new_content}
    </main>
</body></html>"""
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ SUCCÈS : Site mis à jour !")

    except Exception as e:
        print(f"❌ ÉCHEC FINAL : {e}")
        # En cas d'échec total, on ne plante pas le script pour voir les logs
        pass

if __name__ == "__main__":
    main()
