import re
import matplotlib.pyplot as plt

# Fichiers de résultats adaptés à tes noms
FILES = {
    "Partie 1": "resultats.txt",
    "Partie 2": "resultats1.txt",
    "Partie 3": "resultats3.txt",
}

REQUETES = [f"R{i}" for i in range(1, 11)]


def lire_resultats(fichier):
    temps = {r: None for r in REQUETES}
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                m = re.match(r"(R\d+)\s*:\s*(\d+)\s*ms", ligne.strip())
                if m:
                    req = m.group(1)
                    t = int(m.group(2))
                    temps[req] = t
    except FileNotFoundError:
        print(f"Fichier introuvable : {fichier}")
    return temps


def main():
    data = {partie: lire_resultats(f) for partie, f in FILES.items()}

    x = range(len(REQUETES))
    largeur = 0.25

    plt.figure(figsize=(12, 6))

    for i, (partie, temps) in enumerate(data.items()):
        valeurs = [temps[r] if temps[r] is not None else 0 for r in REQUETES]
        positions = [p + i * largeur for p in x]
        plt.bar(positions, valeurs, width=largeur, label=partie)

    positions_centre = [p + largeur for p in x]
    plt.xticks(positions_centre, REQUETES)

    plt.ylabel("Temps d'exécution (ms)")
    plt.title("Comparaison des temps d'exécution R1–R10 (Parties 1, 2, 3)")
    plt.legend()
    plt.tight_layout()

    plt.savefig("comparaison_temps.png")
    plt.show()


if __name__ == "__main__":
    main()