from flask import Flask, render_template, request
import time
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    requete = request.form['requete']
    start_time = time.time()

    fonctions = {
        'R1': traiter_R1,
        'R2': traiter_R2,
        'R3': traiter_R3,
        'R4': traiter_R4,
        'R5': traiter_R5,
        'R6': traiter_R6,
        'R7': traiter_R7,
        'R8': traiter_R8,
        'R9': traiter_R9,
        'R10': traiter_R10,
        'R11': traiter_R11
    }

    resultat = fonctions.get(requete, lambda: "Requête non prise en charge")()
    end_time = time.time()
    temps = round((end_time - start_time) * 1000, 2)

    enregistrer_resultat(requete, resultat, temps)

    return render_template('search.html', resultat=resultat, temps=temps)

def enregistrer_resultat(requete, resultat, temps):
    try:
        with open("resultats.txt", "a", encoding="utf-8") as f:
            f.write(f"{requete} | {temps} ms | {resultat.replace('<br>', ' | ')}\n")
    except Exception as e:
        print(f"Erreur enregistrement : {e}")

def charger_tableau(fichier):
    chemin = os.path.join("site_html", f"{fichier}.html")
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
            soup = BeautifulSoup(contenu, "html.parser")
            return soup.find("table")
    except Exception as e:
        print(f"Erreur lecture fichier {chemin} : {e}")
        return None

def traiter_R1():
    table = charger_tableau("classement")
    if table:
        lignes = table.find_all("tr")[1:]
        if lignes:
            return lignes[0].find_all("td")[1].text.strip()
    return "Erreur : tableau introuvable"

def traiter_R2():
    table = charger_tableau("classement")
    if not table:
        return "Erreur : tableau introuvable"
    total = sum(int(row.find_all("td")[3].text.strip()) for row in table.find_all("tr")[1:] if len(row.find_all("td")) >= 4)
    return f"{total} matchs joués"

def traiter_R3():
    table = charger_tableau("classement")
    if not table:
        return "Erreur : tableau introuvable"
    total_buts = sum(int(row.find_all("td")[7].text.strip()) for row in table.find_all("tr")[1:] if len(row.find_all("td")) >= 8)
    return f"{total_buts} buts marqués"

def traiter_R4():
    table = charger_tableau("classement")
    if not table:
        return "Erreur : tableau introuvable"
    max_buts, equipe = 0, ""
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) >= 8:
            buts = int(cells[7].text.strip())
            if buts > max_buts:
                max_buts = buts
                equipe = cells[1].text.strip()
    return f"{equipe} avec {max_buts} buts"

def traiter_R5():
    table = charger_tableau("classement")
    if not table:
        return "Erreur : tableau introuvable"
    equipes = [f"{row.find_all('td')[1].text.strip()} : {row.find_all('td')[7].text.strip()}" for row in table.find_all("tr")[1:] if len(row.find_all("td")) >= 8 and int(row.find_all("td")[7].text.strip()) > 70]
    return "<br>".join(equipes) if equipes else "Aucune équipe avec plus de 70 buts"

def traiter_R6():
    table = charger_tableau("calendrier")
    if not table:
        return "Erreur : tableau introuvable"
    matchs = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) >= 3 and "novembre" in cells[0].text.lower():
            matchs.append(" - ".join(cell.text.strip() for cell in cells))
    return "<br>".join(matchs) if matchs else "Aucun match en novembre 2008"

def traiter_R7():
    try:
        with open("site_html/teams/equipe_Manchester_United.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            matchs = soup.find_all("div", class_="match-result")
            victoires = [m for m in matchs if "Manchester United" in m.text and "victoire domicile" in m.text.lower()]
            return f"{len(victoires)} victoires à domicile"
    except:
        return "Fichier de Manchester United introuvable"

def traiter_R8():
    table = charger_tableau("classement")
    if not table:
        return "Erreur : tableau introuvable"
    classement = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) >= 6:
            equipe = cells[1].text.strip()
            victoires_ext = int(cells[5].text.strip())
            classement.append((equipe, victoires_ext))
    classement.sort(key=lambda x: x[1], reverse=True)
    return "<br>".join([f"{equipe} : {victoires}" for equipe, victoires in classement])

def traiter_R9():
    table = charger_tableau("classement")
    if not table:
        return "Erreur : tableau introuvable"
    lignes = table.find_all("tr")[1:7]
    total = sum(int(row.find_all("td")[7].text.strip()) for row in lignes if len(row.find_all("td")) >= 8)
    moyenne = round(total / len(lignes), 2)
    return f"Moyenne de buts à l’extérieur du Top 6 : {moyenne}"

def traiter_R10():
    try:
        with open("site_html/teams/equipe_Manchester_United.html", "r", encoding="utf-8") as f1, open("site_html/teams/equipe_Chelsea.html", "r", encoding="utf-8") as f2:
            soup1 = BeautifulSoup(f1.read(), "html.parser")
            soup2 = BeautifulSoup(f2.read(), "html.parser")
            matchs1 = soup1.find_all("div", class_="match-result")
            matchs2 = soup2.find_all("div", class_="match-result")
            confrontations = [m.text.strip() for m in matchs1 + matchs2 if "Chelsea" in m.text or "Manchester United" in m.text]
            return "<br>".join(confrontations) if confrontations else "Aucune confrontation trouvée"
    except:
        return "Pages des équipes manquantes"

def traiter_R11():
    table = charger_tableau("classement")
    if not table:
        return "Erreur : tableau introuvable"
    equipes = []
    for ligne in table.find_all("tr")[1:]:
        cellules = ligne.find_all("td")
        if len(cellules) >= 8:
            nom = cellules[1].text.strip()
            buts = int(cellules[7].text.strip())
            if buts > 40:
                equipes.append(f"{nom} : {buts}")
    return "<br>".join(equipes) if equipes else "Aucune équipe trouvée"

@app.route('/graph')
def graph():
    donnees = []
    try:
        with open("resultats.txt", "r", encoding="utf-8") as f:
            for ligne in f:
                parts = ligne.strip().split("|")
                if len(parts) >= 3:
                    requete = parts[0].strip()
                    temps = float(parts[1].replace("ms", "").strip())
                    donnees.append((requete, temps))
    except:
        return "Aucun résultat enregistré."

    labels = [d[0] for d in donnees]
    valeurs = [d[1] for d in donnees]

    return render_template("graph.html", labels=labels, valeurs=valeurs)

if __name__ == '__main__':
    print("Serveur Flask lancé sur http://127.0.0.1:5000")
    app.run(debug=True)