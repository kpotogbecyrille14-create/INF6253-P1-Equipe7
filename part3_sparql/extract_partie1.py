import re

# Ton fichier brut (Partie 1)
INPUT_FILE = "resultats0.txt"

# Le fichier propre que tu veux générer
OUTPUT_FILE = "resultats.txt"

# Regex pour capturer les lignes du type :
# R3 | 14.47 ms | ...
pattern = re.compile(r"(R\d+)\s*\|\s*([\d\.]+)\s*ms", re.IGNORECASE)

# On veut seulement R1 à R10
REQUETES_VALIDES = {f"R{i}" for i in range(1, 11)}

# Dictionnaire pour stocker les temps
resultats = {}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for ligne in f:
        m = pattern.search(ligne)
        if m:
            req = m.group(1)
            temps = float(m.group(2))

            # On garde seulement R1..R10
            if req in REQUETES_VALIDES:
                # On garde la première occurrence uniquement
                if req not in resultats:
                    resultats[req] = int(round(temps))

# Écriture du fichier propre
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i in range(1, 11):
        req = f"R{i}"
        if req in resultats:
            f.write(f"{req} : {resultats[req]} ms\n")
        else:
            f.write(f"{req} : 0 ms\n")

print("✔ Fichier resultats.txt généré avec succès.")
