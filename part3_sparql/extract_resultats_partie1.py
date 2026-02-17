import re

INPUT_FILE = "R1 _ 23.61 ms _ Manchester United.txt"   # ton fichier brut
OUTPUT_FILE = "resultats1.txt"

# Regex pour capturer les lignes du type :
# R3 | 14.47 ms | ...
pattern = re.compile(r"(R\d+)\s*\|\s*([\d\.]+)\s*ms", re.IGNORECASE)

# On veut seulement R1 à R10
REQUETES_VALIDES = {f"R{i}" for i in range(1, 11)}

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

print("✔ Fichier resultats1.txt généré avec succès.")
