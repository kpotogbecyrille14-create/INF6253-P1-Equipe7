import csv
from read_part1_results import read_part1_results
import re

def read_part2_results():
    temps = {}
    with open("resultats1.txt", "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"(R\d+)\s*:\s*(\d+)\s*ms", line)
            if match:
                req = match.group(1)
                ms = int(match.group(2))
                temps[req] = ms
    return temps

def build_csv():
    p1 = read_part1_results()
    p2 = read_part2_results()

    with open("temps_partie1_partie2.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["requete", "partie1_ms", "partie2_ms"])

        for r in sorted(p1.keys()):
            writer.writerow([r, p1.get(r, ""), p2.get(r, "")])

    print("CSV généré : temps_partie1_partie2.csv")

if __name__ == "__main__":
    build_csv()