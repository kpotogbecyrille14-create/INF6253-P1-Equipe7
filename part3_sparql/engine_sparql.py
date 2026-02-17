from flask import Flask, render_template, request
import time
import requests
import os

app = Flask(__name__)

# URL Fuseki (dataset = premierleague)
FUSEKI_URL = "http://localhost:3030/premierleague/query"

# Dossier contenant les requêtes SPARQL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUERY_DIR = os.path.join(BASE_DIR, "queries")

# Sauvegarde des résultats
def save_result(query_id, result, elapsed):
    with open("resultats3.txt", "a", encoding="utf-8") as f:
        f.write(f"{query_id} : {elapsed} ms\n{result}\n\n")


# ---------------------------------------------------------
# Fonction pour exécuter une requête SPARQL
# ---------------------------------------------------------
def run_sparql(query_id):
    query_file = os.path.join(QUERY_DIR, f"{query_id}.sparql")

    if not os.path.exists(query_file):
        return f"Erreur : fichier {query_id}.sparql introuvable."

    # Lire la requête SPARQL
    with open(query_file, "r", encoding="utf-8") as f:
        query = f.read()

    # Envoyer la requête à Fuseki
    response = requests.post(
        FUSEKI_URL,
        data={"query": query},
        headers={"Accept": "application/sparql-results+json"}
    )

    if response.status_code != 200:
        return f"Erreur Fuseki : {response.status_code}\n{response.text}"

    data = response.json()

    # Convertir les résultats en texte lisible
    results = data.get("results", {}).get("bindings", [])
    if not results:
        return "Aucun résultat."

    output = ""
    for row in results:
        line = " | ".join(v.get("value", "") for v in row.values())
        output += line + "\n"

    return output.strip()


# ---------------------------------------------------------
# Flask : interface web
# ---------------------------------------------------------
QUERIES = [f"R{i}" for i in range(1, 11)]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    elapsed = None
    selected = "R1"

    if request.method == "POST":
        selected = request.form.get("query_id")

        start = time.time()
        result = run_sparql(selected)
        elapsed = int((time.time() - start) * 1000)

        save_result(selected, result, elapsed)

    return render_template("search3.html",
                           queries=QUERIES,
                           selected=selected,
                           result=result,
                           elapsed=elapsed)


if __name__ == "__main__":
    app.run(debug=True)
