import os
from bs4 import BeautifulSoup
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

# Dossiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, "..", "part2_web3_enriched", "site_html_enriched")
OUTPUT_DIR = os.path.join(BASE_DIR, "rdf")

# Création du dossier rdf si absent
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fichier RDF final
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "knowledge_graph.ttl")

# Namespace Schema.org
SCHEMA = Namespace("http://schema.org/")

# Graphe RDF
g = Graph()
g.bind("schema", SCHEMA)


# ---------------------------------------------------------
# Extraction des équipes
# ---------------------------------------------------------
def extract_teams():
    teams = []

    for filename in os.listdir(HTML_DIR):
        if not filename.endswith(".html"):
            continue

        path = os.path.join(HTML_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # On ne garde que les pages contenant un classement
        if "Classement" not in soup.text:
            continue

        for row in soup.find_all(attrs={"typeof": "SportsTeam"}):
            team = {}

            for cell in row.find_all(attrs={"property": True}):
                prop = cell["property"]
                value = cell.get_text(strip=True)
                team[prop] = value

            if "name" in team:
                teams.append(team)

    return teams


# ---------------------------------------------------------
# Extraction des matchs
# ---------------------------------------------------------
def extract_matches():
    matches = []

    for filename in os.listdir(HTML_DIR):
        if not filename.endswith(".html"):
            continue

        path = os.path.join(HTML_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # On ne garde que les pages calendrier
        if "Calendrier des matchs" not in soup.text:
            continue

        for row in soup.find_all(attrs={"typeof": "SportsEvent"}):
            match = {}

            date_cell = row.find(attrs={"property": "startDate"})
            home_cell = row.find(attrs={"property": "homeTeam"})
            away_cell = row.find(attrs={"property": "awayTeam"})
            score_cell = row.find(attrs={"property": "score"})

            if not (date_cell and home_cell and away_cell and score_cell):
                continue

            match["date"] = date_cell.get_text(strip=True)
            match["homeTeam"] = home_cell.get_text(strip=True)
            match["awayTeam"] = away_cell.get_text(strip=True)

            score = score_cell.get_text(strip=True)
            if "-" not in score:
                continue

            h, a = score.split("-")
            match["homeGoals"] = h.strip()
            match["awayGoals"] = a.strip()

            matches.append(match)

    return matches


# ---------------------------------------------------------
# Construction du graphe RDF
# ---------------------------------------------------------
def build_graph():
    teams = extract_teams()
    matches = extract_matches()

    # Ajout des équipes
    for t in teams:
        uri = URIRef(f"http://example.org/team/{t['name'].replace(' ', '_')}")
        g.add((uri, RDF.type, SCHEMA.SportsTeam))

        for key, value in t.items():
            g.add((uri, SCHEMA[key], Literal(value)))

    # Ajout des matchs
    for m in matches:
        uri = URIRef(f"http://example.org/match/{m['date'].replace('/', '-')}_{m['homeTeam'].replace(' ', '_')}_vs_{m['awayTeam'].replace(' ', '_')}")
        g.add((uri, RDF.type, SCHEMA.SportsEvent))

        g.add((uri, SCHEMA.startDate, Literal(m["date"], datatype=XSD.string)))
        g.add((uri, SCHEMA.homeTeam, Literal(m["homeTeam"])))
        g.add((uri, SCHEMA.awayTeam, Literal(m["awayTeam"])))
        g.add((uri, SCHEMA.homeTeamScore, Literal(m["homeGoals"], datatype=XSD.integer)))
        g.add((uri, SCHEMA.awayTeamScore, Literal(m["awayGoals"], datatype=XSD.integer)))

    # Sauvegarde
    g.serialize(destination=OUTPUT_FILE, format="turtle")
    print(f"✔ knowledge_graph.ttl généré dans {OUTPUT_DIR}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    build_graph()
