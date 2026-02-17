import matplotlib.pyplot as plt
import csv

CSV_PATH = "temps_partie1_partie2.csv"

reqs = []
p1 = []
p2 = []

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        r = row["requete"]
        v1 = row["partie1_ms"]
        v2 = row["partie2_ms"]

        # On ignore les lignes où les deux valeurs sont vides
        if v1 == "" and v2 == "":
            continue

        reqs.append(r)
        p1.append(float(v1) if v1 != "" else 0)
        p2.append(float(v2) if v2 != "" else 0)

x = range(len(reqs))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar([i - width/2 for i in x], p1, width=width, label="Partie 1")
plt.bar([i + width/2 for i in x], p2, width=width, label="Partie 2")

plt.xticks(x, reqs)
plt.ylabel("Temps (ms)")
plt.title("Comparaison des temps de recherche - Partie 1 vs Partie 2")
plt.legend()
plt.tight_layout()

out_path = "comparaison_partie1_partie2.png"
plt.savefig(out_path)
print("Graphique sauvegardé :", out_path)