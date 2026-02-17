from flask import Flask, render_template, request
import time
from utils_rdfa import extract_teams, extract_matches, to_int

app = Flask(__name__)

# Sauvegarde automatique
def save_result(query_id, result, elapsed):
    with open("resultats1.txt", "a", encoding="utf-8") as f:
        f.write(f"{query_id} : {elapsed} ms\n{result}\n\n")


# ---------------------------------------------------------
# R1 : Quelle équipe est première au classement ?
# ---------------------------------------------------------
def R1():
    teams = extract_teams()
    teams_sorted = sorted(teams, key=lambda t: to_int(t.get("position", "999")))
    return teams_sorted[0].get("name", "Inconnu")


# ---------------------------------------------------------
# R2 : Combien de matchs ont été joués ?
# ---------------------------------------------------------
def R2():
    return str(len(extract_matches()))


# ---------------------------------------------------------
# R3 : Nombre total de buts marqués
# ---------------------------------------------------------
def R3():
    total = 0
    for m in extract_matches():
        total += to_int(m.get("homeGoals", "0")) + to_int(m.get("awayGoals", "0"))
    return str(total)


# ---------------------------------------------------------
# R4 : Équipe ayant marqué le plus de buts
# ---------------------------------------------------------
def R4():
    teams = extract_teams()
    best = max(teams, key=lambda t: to_int(t.get("goalsScored", "0")))
    return f"{best['name']} : {best['goalsScored']}"


# ---------------------------------------------------------
# R5 : Équipes ayant marqué plus de 70 buts
# ---------------------------------------------------------
def R5():
    teams = extract_teams()
    res = [f"{t['name']} : {t['goalsScored']}" for t in teams if to_int(t.get("goalsScored", "0")) > 70]
    return "\n".join(res) if res else "Aucune équipe"


# ---------------------------------------------------------
# R6 : Matchs de novembre 2008
# ---------------------------------------------------------
def R6():
    res = []
    for m in extract_matches():
        date = m.get("date", "")
        if "/11/2008" in date:
            score = f"{m.get('homeGoals')} - {m.get('awayGoals')}"
            res.append(f"{date} : {m['homeTeam']} {score} {m['awayTeam']}")
    return "\n".join(res) if res else "Aucun match"


# ---------------------------------------------------------
# R7 : Victoires à domicile de Manchester United
# ---------------------------------------------------------
def R7():
    count = 0
    for m in extract_matches():
        if m.get("homeTeam") == "Manchester United":
            if to_int(m.get("homeGoals", "0")) > to_int(m.get("awayGoals", "0")):
                count += 1
    return str(count)


# ---------------------------------------------------------
# R8 : Classement des équipes par victoires à l’extérieur
# ---------------------------------------------------------
def R8():
    wins = {}
    for m in extract_matches():
        away = m.get("awayTeam")
        if to_int(m.get("awayGoals", "0")) > to_int(m.get("homeGoals", "0")):
            wins[away] = wins.get(away, 0) + 1

    sorted_wins = sorted(wins.items(), key=lambda x: x[1], reverse=True)
    return "\n".join(f"{team} : {nb}" for team, nb in sorted_wins) if sorted_wins else "Aucune victoire à l'extérieur"


# ---------------------------------------------------------
# R9 : Moyenne de buts à l’extérieur du Top 6
# ---------------------------------------------------------
def R9():
    teams = extract_teams()
    top6 = [t["name"] for t in sorted(teams, key=lambda t: to_int(t.get("position", "999")))[:6]]

    total = 0
    count = 0
    for m in extract_matches():
        if m.get("awayTeam") in top6:
            total += to_int(m.get("awayGoals", "0"))
            count += 1

    return f"{total/count:.2f}" if count else "0"


# ---------------------------------------------------------
# R10 : Confrontations 1er vs 3e
# ---------------------------------------------------------
def R10():
    teams = extract_teams()
    sorted_teams = sorted(teams, key=lambda t: to_int(t.get("position", "999")))

    first = sorted_teams[0]["name"]
    third = sorted_teams[2]["name"]

    res = []
    for m in extract_matches():
        if {m.get("homeTeam"), m.get("awayTeam")} == {first, third}:
            score = f"{m.get('homeGoals')} - {m.get('awayGoals')}"
            res.append(f"{m['date']} : {m['homeTeam']} {score} {m['awayTeam']}")

    return "\n".join(res) if res else "Aucune confrontation"


# ---------------------------------------------------------
# Flask
# ---------------------------------------------------------
QUERIES = {
    "R1": R1, "R2": R2, "R3": R3, "R4": R4, "R5": R5,
    "R6": R6, "R7": R7, "R8": R8, "R9": R9, "R10": R10
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    elapsed = None
    selected = "R1"

    if request.method == "POST":
        selected = request.form.get("query_id")
        func = QUERIES[selected]

        start = time.time()
        result = func()
        elapsed = int((time.time() - start) * 1000)

        save_result(selected, result, elapsed)

    return render_template("search2.html",
                           queries=QUERIES.keys(),
                           selected=selected,
                           result=result,
                           elapsed=elapsed)

if __name__ == "__main__":
    app.run(debug=True)