import os
from bs4 import BeautifulSoup

# Dossier contenant les fichiers enrichis
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENRICHED_DIR = os.path.join(BASE_DIR, "site_html_enriched")


# ---------------------------------------------------------
# Charger toutes les pages HTML enrichies
# ---------------------------------------------------------
def load_all_pages():
    soups = []
    for root, _, files in os.walk(ENRICHED_DIR):
        for name in files:
            if name.endswith(".html"):
                path = os.path.join(root, name)
                with open(path, "r", encoding="utf-8") as f:
                    soups.append(BeautifulSoup(f.read(), "html.parser"))
    return soups


# ---------------------------------------------------------
# Extraction des équipes (classement)
# ---------------------------------------------------------
def extract_teams():
    soups = load_all_pages()
    teams = []

    for soup in soups:
        # On ne garde que les pages contenant un classement
        if "Classement" not in soup.text:
            continue

        for row in soup.find_all(attrs={"typeof": "SportsTeam"}):
            team = {}

            for cell in row.find_all(attrs={"property": True}):
                prop = cell["property"]
                value = cell.get_text(strip=True)
                team[prop] = value

            # On ne garde que les vraies équipes du classement
            if "position" in team:
                teams.append(team)

    return teams


# ---------------------------------------------------------
# Extraction des matchs (calendrier)
# ---------------------------------------------------------
def extract_matches():
    soups = load_all_pages()
    matches = []

    for soup in soups:
        # On ne garde que les pages calendrier
        if "Calendrier des matchs" not in soup.text:
            continue

        for row in soup.find_all(attrs={"typeof": "SportsEvent"}):
            match = {}

            # Date
            date_cell = row.find(attrs={"property": "startDate"})
            if not date_cell:
                continue
            match["date"] = date_cell.get_text(strip=True)

            # Home team
            home_cell = row.find(attrs={"property": "homeTeam"})
            if not home_cell:
                continue
            match["homeTeam"] = home_cell.get_text(strip=True)

            # Away team
            away_cell = row.find(attrs={"property": "awayTeam"})
            if not away_cell:
                continue
            match["awayTeam"] = away_cell.get_text(strip=True)

            # Score "X - Y"
            score_cell = row.find(attrs={"property": "score"})
            if not score_cell:
                continue

            score_text = score_cell.get_text(strip=True)
            if "-" not in score_text:
                continue

            h, a = score_text.split("-")
            match["homeGoals"] = h.strip()
            match["awayGoals"] = a.strip()

            matches.append(match)

    return matches


# ---------------------------------------------------------
# Conversion sécurisée en entier
# ---------------------------------------------------------
def to_int(value, default=0):
    try:
        return int(value)
    except:
        try:
            return int(value.replace("+", "").replace("-", ""))
        except:
            return default